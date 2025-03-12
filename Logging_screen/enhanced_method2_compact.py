import sqlite3
import datetime
import os
import uuid
import hashlib
import json
import logging
from cryptography.fernet import Fernet
import threading
import time

class CompactDBLogger:
    """Sistema di logging compatto basato su database SQLite con archiviazione automatica e conformità GDPR/HIPAA."""
    
    def __init__(self, db_path="logs.db", archive_days=30, retention_days=90):
        """Inizializza il logger compatto basato su database."""
        # Setup base
        self.db_path = db_path
        self.archive_days = archive_days
        self.retention_days = retention_days
        self.archive_dir = "log_archives"
        os.makedirs(self.archive_dir, exist_ok=True)
        
        # Crittografia - genera una chiave e salva in un file
        key_dir = os.path.dirname(db_path) or "."
        key_file = os.path.join(key_dir, ".db_key")
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)
        
        # Inizializza database
        self._init_database()
        
        # Avvia thread di manutenzione
        self.stop_thread = False
        self.maintenance_thread = threading.Thread(target=self._maintenance_worker)
        self.maintenance_thread.daemon = True
        self.maintenance_thread.start()
    
    def _init_database(self):
        """Inizializza la struttura del database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabella principale dei log
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        log_id TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        level TEXT NOT NULL,
                        component TEXT NOT NULL,
                        user_id_hash TEXT,
                        message TEXT NOT NULL,
                        encrypted INTEGER DEFAULT 0,
                        metadata TEXT
                    )
                """)
                
                # Indici per prestazioni
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs (timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_level ON logs (level)")
                
                # Tabella per audit trail
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS log_access (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        user TEXT NOT NULL,
                        action TEXT NOT NULL,
                        details TEXT
                    )
                """)
                
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Errore database: {e}")
    
    def _maintenance_worker(self):
        """Thread di manutenzione che esegue archiviazione e pulizia periodica."""
        while not self.stop_thread:
            try:
                # Esegui manutenzione ogni giorno
                self.archive_old_logs()
                self.cleanup_archived_logs()
            except Exception as e:
                logging.error(f"Errore manutenzione: {e}")
                
            # Dormi per 24 ore (86400 secondi)
            for _ in range(86400):
                if self.stop_thread:
                    break
                time.sleep(1)
    
    def log(self, level, message, user_id=None, component="general", 
            sensitive_data=None, additional_data=None, encrypt_message=False):
        """Registra un messaggio di log nel database con metadati avanzati."""
        try:
            # Genera ID e timestamp
            log_id = str(uuid.uuid4())
            timestamp = datetime.datetime.now().isoformat()
            
            # Hash user_id se presente
            user_id_hash = hashlib.sha256(str(user_id).encode()).hexdigest() if user_id else None
            
            # Prepara metadati
            metadata = {}
            if additional_data:
                metadata.update(additional_data)
            if sensitive_data:
                metadata["sensitive_data_hash"] = hashlib.sha256(str(sensitive_data).encode()).hexdigest()
            
            # Serializza metadati
            metadata_json = json.dumps(metadata) if metadata else None
            
            # Cripta messaggio se richiesto
            if encrypt_message:
                message = self.cipher.encrypt(message.encode()).decode()
            
            # Inserisci log
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO logs 
                    (log_id, timestamp, level, component, user_id_hash, message, encrypted, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (log_id, timestamp, level.upper(), component, user_id_hash, 
                     message, encrypt_message, metadata_json)
                )
                conn.commit()
            
            return log_id
        except sqlite3.Error as e:
            logging.error(f"Errore logging: {e}")
            return None
    
    def archive_old_logs(self):
        """Archivia i log più vecchi dell'intervallo configurato in un database separato."""
        try:
            # Calcola soglia
            archive_threshold = datetime.datetime.now() - datetime.timedelta(days=self.archive_days)
            archive_threshold_str = archive_threshold.isoformat()
            
            # Nome archivio
            archive_date = datetime.datetime.now().strftime("%Y%m%d")
            archive_file = os.path.join(self.archive_dir, f"logs_archive_{archive_date}.db")
            
            with sqlite3.connect(self.db_path) as conn:
                # Verifica se ci sono log da archiviare
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM logs WHERE timestamp <= ?", (archive_threshold_str,))
                count = cursor.fetchone()[0]
                
                if count == 0:
                    return  # Nessun log da archiviare
                
                # Crea database di archivio
                with sqlite3.connect(archive_file) as archive_conn:
                    conn.backup(archive_conn)
                    
                    # Mantieni solo log vecchi nell'archivio
                    archive_cursor = archive_conn.cursor()
                    archive_cursor.execute("DELETE FROM logs WHERE timestamp > ?", (archive_threshold_str,))
                    archive_conn.commit()
                    
                    # Elimina log archiviati dal database principale
                    cursor.execute("DELETE FROM logs WHERE timestamp <= ?", (archive_threshold_str,))
                    conn.commit()
                    
                    # Registra operazione
                    self._log_access("SYSTEM", "ARCHIVE", f"Archiviati {count} log in {archive_file}")
                    print(f"Archiviati {count} log in {archive_file}")
        except Exception as e:
            logging.error(f"Errore archiviazione: {e}")
    
    def cleanup_archived_logs(self):
        """Elimina gli archivi di log più vecchi del periodo di conservazione configurato."""
        try:
            # Calcola soglia
            retention_threshold = datetime.datetime.now() - datetime.timedelta(days=self.retention_days)
            
            # Controlla archivi
            for filename in os.listdir(self.archive_dir):
                if not filename.startswith("logs_archive_"):
                    continue
                    
                file_path = os.path.join(self.archive_dir, filename)
                
                # Estrai data
                try:
                    date_str = filename.replace("logs_archive_", "").replace(".db", "")
                    file_date = datetime.datetime.strptime(date_str, "%Y%m%d")
                    
                    # Elimina se vecchio
                    if file_date < retention_threshold:
                        os.remove(file_path)
                        print(f"Archivio eliminato: {filename}")
                        self._log_access("SYSTEM", "DELETE", f"Eliminato archivio {filename}")
                except (ValueError, OSError) as e:
                    logging.error(f"Errore pulizia: {e}")
        except Exception as e:
            logging.error(f"Errore pulizia archivi: {e}")
    
    def _log_access(self, user, action, details=None):
        """Registra un accesso o un'operazione sui log per l'audit trail."""
        try:
            timestamp = datetime.datetime.now().isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO log_access (timestamp, user, action, details) VALUES (?, ?, ?, ?)",
                    (timestamp, user, action, details)
                )
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Errore audit: {e}")
    
    def query_logs(self, start_date=None, end_date=None, level=None, 
                  component=None, user_id=None, limit=100, decrypt=False):
        """Esegue una query sui log con vari filtri."""
        try:
            # Costruisci query
            query = "SELECT * FROM logs WHERE 1=1"
            params = []
            
            # Filtri
            if start_date:
                start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d").isoformat()
                query += " AND timestamp >= ?"
                params.append(start_dt)
                
            if end_date:
                end_dt = (datetime.datetime.strptime(end_date, "%Y-%m-%d") + 
                          datetime.timedelta(days=1)).isoformat()
                query += " AND timestamp < ?"
                params.append(end_dt)
                
            if level:
                query += " AND level = ?"
                params.append(level.upper())
                
            if component:
                query += " AND component = ?"
                params.append(component)
                
            if user_id:
                user_id_hash = hashlib.sha256(str(user_id).encode()).hexdigest()
                query += " AND user_id_hash = ?"
                params.append(user_id_hash)
            
            # Ordina e limita
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            # Esegui query
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Registra accesso
                self._log_access("API", "QUERY", f"Query con filtri: {json.dumps({'start': start_date, 'end': end_date, 'level': level})}")
                
                # Processa risultati
                results = []
                for row in rows:
                    log_entry = dict(row)
                    
                    # Decripta se necessario
                    if decrypt and log_entry.get("encrypted"):
                        try:
                            log_entry["message"] = self.cipher.decrypt(log_entry["message"].encode()).decode()
                        except Exception:
                            log_entry["message"] = "[Messaggio criptato]"
                    
                    # Converti metadati
                    if log_entry.get("metadata"):
                        log_entry["metadata"] = json.loads(log_entry["metadata"])
                    
                    results.append(log_entry)
                
                return results
        except Exception as e:
            logging.error(f"Errore query: {e}")
            return []
    
    def export_logs_for_analysis(self, output_file=None, format="csv", decrypt=False, **query_params):
        """Esporta i log in un formato adatto all'analisi."""
        # Ottieni log
        logs = self.query_logs(decrypt=decrypt, **query_params)
        
        if not logs:
            print("Nessun log da esportare")
            return None
        
        # Nome file
        if not output_file:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            output_file = f"logs_export_{today}.{format}"
        
        try:
            if format.lower() == "csv":
                import csv
                
                # Determina chiavi
                all_keys = set()
                for log in logs:
                    all_keys.update(log.keys())
                    if "metadata" in log and isinstance(log["metadata"], dict):
                        all_keys.update(f"metadata_{k}" for k in log["metadata"].keys())
                
                if "metadata" in all_keys:
                    all_keys.remove("metadata")
                
                headers = sorted(all_keys)
                
                # Scrivi CSV
                with open(output_file, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()
                    
                    for log in logs:
                        log_row = log.copy()
                        
                        # Espandi metadati
                        if "metadata" in log_row and isinstance(log_row["metadata"], dict):
                            for k, v in log_row["metadata"].items():
                                log_row[f"metadata_{k}"] = v
                            del log_row["metadata"]
                        
                        writer.writerow(log_row)
            
            elif format.lower() == "json":
                with open(output_file, 'w') as jsonfile:
                    json.dump(logs, jsonfile, indent=2)
            
            else:
                raise ValueError(f"Formato non supportato: {format}")
            
            # Registra esportazione
            self._log_access("API", "EXPORT", f"Esportati {len(logs)} log in {output_file}")
            
            print(f"Esportati {len(logs)} log in {output_file}")
            return output_file
            
        except Exception as e:
            logging.error(f"Errore esportazione: {e}")
            return None
    
    def stop(self):
        """Ferma il thread di manutenzione."""
        self.stop_thread = True
        if self.maintenance_thread.is_alive():
            self.maintenance_thread.join(timeout=1)

def test_compact_db_logger():
    """Test del logger compatto basato su database."""
    # Inizializza logger
    logger = CompactDBLogger(db_path="compact_logs.db", archive_days=30, retention_days=90)
    
    # Log di esempio
    logger.log("info", "Applicazione avviata", component="system")
    logger.log("info", "Login utente", user_id="user123", component="auth")
    logger.log("warning", "Tentativo fallito", user_id="user456", component="auth", 
              additional_data={"ip": "192.168.1.1", "attempts": 3})
    logger.log("error", "Dati carta di credito", user_id="user123", component="payment", 
              sensitive_data="4111-1111-1111-1111", additional_data={"amount": 99.99})
    logger.log("critical", "Dati sensibili", user_id="admin", component="security", encrypt_message=True)
    
    # Query e export
    print("\nQuery dei log:")
    logs = logger.query_logs(level="INFO", limit=10)
    for log in logs:
        print(f"{log['timestamp']} - {log['level']} - {log['message']}")
    
    # Esporta log normali
    export_path = logger.export_logs_for_analysis(format="csv", level="INFO")
    print(f"\nLog esportati in: {export_path}")
    
    # Esporta log con decrittazione
    secure_export_path = logger.export_logs_for_analysis(format="csv", decrypt=True)
    print(f"\nLog decriptati esportati in: {secure_export_path}")
    
    # Manutenzione manuale
    logger.archive_old_logs()
    
    # Ferma thread
    logger.stop()
    
    return logger

if __name__ == "__main__":
    test_compact_db_logger() 