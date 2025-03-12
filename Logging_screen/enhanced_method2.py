import sqlite3
import datetime
import os
import uuid
import hashlib
import json
import logging
from cryptography.fernet import Fernet
import schedule
import time
import threading

class EnhancedDBLogger:
    """
    Sistema di logging avanzato basato su database SQLite con archiviazione automatica,
    conformità GDPR/HIPAA e struttura migliorata per l'analisi.
    """
    
    def __init__(self, db_path="logs.db", archive_interval_days=30, 
                 retention_days=90, encryption_key=None):
        """
        Inizializza il logger avanzato basato su database.
        
        :param db_path: Percorso del database SQLite
        :param archive_interval_days: Intervallo in giorni per l'archiviazione automatica
        :param retention_days: Giorni di conservazione dei log prima dell'eliminazione
        :param encryption_key: Chiave di crittografia (generata se None)
        """
        self.db_path = db_path
        self.archive_interval_days = archive_interval_days
        self.retention_days = retention_days
        
        # Directory per gli archivi
        self.archive_dir = "log_archives"
        os.makedirs(self.archive_dir, exist_ok=True)
        
        # Configurazione della crittografia
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Inizializza il database
        self._init_database()
        
        # Configura il job di manutenzione automatica
        self._setup_maintenance_job()
    
    def _init_database(self):
        """Inizializza la struttura del database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabella principale dei log con struttura avanzata
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        log_id TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        level TEXT NOT NULL,
                        component TEXT NOT NULL,
                        user_id_hash TEXT,
                        message TEXT NOT NULL,
                        encrypted BOOLEAN DEFAULT 0,
                        metadata TEXT
                    )
                """)
                
                # Indici per migliorare le prestazioni delle query
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs (timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_level ON logs (level)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_component ON logs (component)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_log_id ON logs (log_id)")
                
                # Tabella per il controllo degli accessi
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
            logging.error(f"Errore durante l'inizializzazione del database: {e}")
    
    def _setup_maintenance_job(self):
        """Configura i job di manutenzione automatica."""
        # Pianifica l'archiviazione automatica ogni giorno a mezzanotte
        schedule.every().day.at("00:00").do(self.archive_old_logs)
        
        # Pianifica la pulizia dei log molto vecchi ogni settimana
        schedule.every().monday.at("01:00").do(self.cleanup_archived_logs)
        
        # Avvia un thread separato per eseguire i job pianificati
        self.stop_scheduler = False
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
    
    def _run_scheduler(self):
        """Esegue lo scheduler in un thread separato."""
        while not self.stop_scheduler:
            schedule.run_pending()
            time.sleep(60)  # Controlla ogni minuto
    
    def _generate_log_id(self):
        """Genera un ID univoco per il log."""
        return str(uuid.uuid4())
    
    def _hash_sensitive_data(self, data):
        """Applica l'hashing ai dati sensibili."""
        if not data:
            return None
        return hashlib.sha256(str(data).encode()).hexdigest()
    
    def _encrypt_message(self, message):
        """Cripta il messaggio di log."""
        return self.cipher.encrypt(message.encode()).decode()
    
    def _decrypt_message(self, encrypted_message):
        """Decripta il messaggio di log."""
        try:
            return self.cipher.decrypt(encrypted_message.encode()).decode()
        except Exception:
            return "[Messaggio criptato]"
    
    def log(self, level, message, user_id=None, component="general", 
            sensitive_data=None, additional_data=None, encrypt_message=False):
        """
        Registra un messaggio di log nel database con metadati avanzati.
        
        :param level: Livello di log (info, warning, error, critical)
        :param message: Messaggio principale del log
        :param user_id: ID dell'utente (opzionale, anonimizzato se presente)
        :param component: Componente del sistema che genera il log
        :param sensitive_data: Dati sensibili da proteggere (verranno hashati)
        :param additional_data: Dati aggiuntivi in formato dizionario
        :param encrypt_message: Se True, il messaggio viene criptato
        """
        try:
            # Genera un ID univoco per il log
            log_id = self._generate_log_id()
            
            # Timestamp corrente in formato ISO
            timestamp = datetime.datetime.now().isoformat()
            
            # Anonimizza l'ID utente se presente
            user_id_hash = self._hash_sensitive_data(user_id) if user_id else None
            
            # Prepara i metadati
            metadata = {}
            if additional_data:
                metadata.update(additional_data)
            
            # Aggiungi dati sensibili hashati se presenti
            if sensitive_data:
                metadata["sensitive_data_hash"] = self._hash_sensitive_data(sensitive_data)
            
            # Serializza i metadati in JSON
            metadata_json = json.dumps(metadata) if metadata else None
            
            # Cripta il messaggio se richiesto
            if encrypt_message:
                message = self._encrypt_message(message)
            
            # Inserisci il log nel database
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
            logging.error(f"Errore durante il logging su database: {e}")
            return None
    
    def archive_old_logs(self):
        """
        Archivia i log più vecchi dell'intervallo configurato in un database separato.
        """
        try:
            # Calcola la data limite per l'archiviazione
            archive_threshold = datetime.datetime.now() - datetime.timedelta(days=self.archive_interval_days)
            archive_threshold_str = archive_threshold.isoformat()
            
            # Nome del file di archivio
            archive_date = datetime.datetime.now().strftime("%Y%m%d")
            archive_file = os.path.join(self.archive_dir, f"logs_archive_{archive_date}.db")
            
            # Connessione al database principale
            with sqlite3.connect(self.db_path) as conn:
                # Crea una connessione al database di archivio
                with sqlite3.connect(archive_file) as archive_conn:
                    # Copia la struttura del database
                    conn.backup(archive_conn)
                    
                    # Elimina i log recenti dal database di archivio (mantieni solo quelli vecchi)
                    archive_cursor = archive_conn.cursor()
                    archive_cursor.execute("DELETE FROM logs WHERE timestamp > ?", (archive_threshold_str,))
                    archive_conn.commit()
                    
                    # Conta quanti log sono stati archiviati
                    archive_cursor.execute("SELECT COUNT(*) FROM logs")
                    archived_count = archive_cursor.fetchone()[0]
                    
                    # Elimina i log archiviati dal database principale
                    if archived_count > 0:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM logs WHERE timestamp <= ?", (archive_threshold_str,))
                        conn.commit()
                        
                        # Registra l'operazione di archiviazione
                        self._log_access("SYSTEM", "ARCHIVE", 
                                        f"Archiviati {archived_count} log in {archive_file}")
                        
                        print(f"Archiviati {archived_count} log in {archive_file}")
                    else:
                        # Se non ci sono log da archiviare, elimina il file di archivio vuoto
                        archive_conn.close()
                        os.remove(archive_file)
                        print("Nessun log da archiviare")
        except Exception as e:
            logging.error(f"Errore durante l'archiviazione dei log: {e}")
    
    def cleanup_archived_logs(self):
        """
        Elimina gli archivi di log più vecchi del periodo di conservazione configurato.
        """
        try:
            # Calcola la data limite per la conservazione
            retention_threshold = datetime.datetime.now() - datetime.timedelta(days=self.retention_days)
            
            # Controlla tutti i file nella directory degli archivi
            for filename in os.listdir(self.archive_dir):
                if not filename.startswith("logs_archive_"):
                    continue
                    
                file_path = os.path.join(self.archive_dir, filename)
                
                # Estrai la data dall'archivio (formato: logs_archive_YYYYMMDD.db)
                try:
                    date_str = filename.replace("logs_archive_", "").replace(".db", "")
                    file_date = datetime.datetime.strptime(date_str, "%Y%m%d")
                    
                    # Elimina l'archivio se è più vecchio della soglia di conservazione
                    if file_date < retention_threshold:
                        os.remove(file_path)
                        print(f"Archivio di log eliminato: {filename}")
                        
                        # Registra l'operazione di eliminazione
                        self._log_access("SYSTEM", "DELETE", f"Eliminato archivio {filename}")
                except (ValueError, OSError) as e:
                    logging.error(f"Errore durante la pulizia dell'archivio {filename}: {e}")
        except Exception as e:
            logging.error(f"Errore durante la pulizia degli archivi: {e}")
    
    def _log_access(self, user, action, details=None):
        """
        Registra un accesso o un'operazione sui log per l'audit trail.
        
        :param user: Utente che ha effettuato l'operazione
        :param action: Tipo di operazione (VIEW, EXPORT, ARCHIVE, DELETE)
        :param details: Dettagli aggiuntivi sull'operazione
        """
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
            logging.error(f"Errore durante la registrazione dell'accesso: {e}")
    
    def query_logs(self, start_date=None, end_date=None, level=None, 
                  component=None, user_id=None, limit=100, decrypt=False):
        """
        Esegue una query sui log con vari filtri.
        
        :param start_date: Data di inizio (formato: YYYY-MM-DD)
        :param end_date: Data di fine (formato: YYYY-MM-DD)
        :param level: Filtra per livello di log
        :param component: Filtra per componente
        :param user_id: Filtra per ID utente (verrà hashato)
        :param limit: Numero massimo di risultati
        :param decrypt: Se True, decripta i messaggi criptati
        :return: Lista di dizionari con i log
        """
        try:
            # Costruisci la query SQL con i filtri
            query = "SELECT * FROM logs WHERE 1=1"
            params = []
            
            # Aggiungi i filtri se specificati
            if start_date:
                start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d").isoformat()
                query += " AND timestamp >= ?"
                params.append(start_dt)
                
            if end_date:
                end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                # Aggiungi un giorno per includere l'intero giorno di fine
                end_dt = (end_dt + datetime.timedelta(days=1)).isoformat()
                query += " AND timestamp < ?"
                params.append(end_dt)
                
            if level:
                query += " AND level = ?"
                params.append(level.upper())
                
            if component:
                query += " AND component = ?"
                params.append(component)
                
            if user_id:
                user_id_hash = self._hash_sensitive_data(user_id)
                query += " AND user_id_hash = ?"
                params.append(user_id_hash)
            
            # Ordina per timestamp decrescente e limita i risultati
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            # Esegui la query
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Registra l'accesso
                self._log_access("API", "QUERY", 
                                f"Query con filtri: {json.dumps({'start': start_date, 'end': end_date, 'level': level, 'component': component})}")
                
                # Converti i risultati in dizionari
                results = []
                for row in rows:
                    log_entry = dict(row)
                    
                    # Decripta il messaggio se richiesto e se è criptato
                    if decrypt and log_entry.get("encrypted"):
                        log_entry["message"] = self._decrypt_message(log_entry["message"])
                    
                    # Converti i metadati JSON in dizionario
                    if log_entry.get("metadata"):
                        log_entry["metadata"] = json.loads(log_entry["metadata"])
                    
                    results.append(log_entry)
                
                return results
        except Exception as e:
            logging.error(f"Errore durante la query dei log: {e}")
            return []
    
    def export_logs_for_analysis(self, output_file=None, format="csv", **query_params):
        """
        Esporta i log in un formato adatto all'analisi.
        
        :param output_file: File di output (default: logs_export_YYYY-MM-DD.{format})
        :param format: Formato di esportazione (csv o json)
        :param query_params: Parametri di query (start_date, end_date, level, component, ecc.)
        :return: Percorso del file esportato
        """
        # Ottieni i log con i parametri specificati
        logs = self.query_logs(**query_params)
        
        if not logs:
            print("Nessun log da esportare")
            return None
        
        # Nome file di default
        if not output_file:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            output_file = f"logs_export_{today}.{format}"
        
        try:
            if format.lower() == "csv":
                import csv
                
                # Determina tutte le chiavi possibili dai log
                all_keys = set()
                for log in logs:
                    all_keys.update(log.keys())
                    if "metadata" in log and isinstance(log["metadata"], dict):
                        all_keys.update(f"metadata_{k}" for k in log["metadata"].keys())
                
                # Rimuovi metadata dalla lista delle chiavi (verrà espanso)
                if "metadata" in all_keys:
                    all_keys.remove("metadata")
                
                # Converti le chiavi in una lista ordinata
                headers = sorted(all_keys)
                
                # Scrivi il file CSV
                with open(output_file, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=headers)
                    writer.writeheader()
                    
                    for log in logs:
                        # Crea una copia del log per la manipolazione
                        log_row = log.copy()
                        
                        # Espandi i metadati
                        if "metadata" in log_row and isinstance(log_row["metadata"], dict):
                            for k, v in log_row["metadata"].items():
                                log_row[f"metadata_{k}"] = v
                            del log_row["metadata"]
                        
                        # Scrivi la riga
                        writer.writerow(log_row)
            
            elif format.lower() == "json":
                with open(output_file, 'w') as jsonfile:
                    json.dump(logs, jsonfile, indent=2)
            
            else:
                raise ValueError(f"Formato non supportato: {format}")
            
            # Registra l'esportazione
            self._log_access("API", "EXPORT", f"Esportati {len(logs)} log in {output_file}")
            
            print(f"Esportati {len(logs)} log in {output_file}")
            return output_file
            
        except Exception as e:
            logging.error(f"Errore durante l'esportazione dei log: {e}")
            return None
    
    def stop(self):
        """Ferma lo scheduler e chiude le risorse."""
        self.stop_scheduler = True
        if self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=1)

# Funzione di test per dimostrare l'uso del logger avanzato
def test_enhanced_db_logger():
    """Testa le funzionalità del logger avanzato basato su database."""
    # Inizializza il logger
    logger = EnhancedDBLogger(db_path="enhanced_logs.db", 
                             archive_interval_days=30, 
                             retention_days=90)
    
    # Registra alcuni log di esempio
    logger.log("info", "Applicazione avviata", component="system")
    logger.log("info", "Utente ha effettuato l'accesso", user_id="user123", component="auth")
    logger.log("warning", "Tentativo di accesso fallito", user_id="user456", 
              component="auth", additional_data={"ip": "192.168.1.1", "attempts": 3})
    logger.log("error", "Errore durante l'elaborazione del pagamento", 
              user_id="user123", component="payment", 
              sensitive_data="4111-1111-1111-1111", 
              additional_data={"amount": 99.99, "currency": "EUR"})
    
    # Log con messaggio criptato
    logger.log("critical", "Informazioni molto sensibili", 
              user_id="admin", component="security", 
              encrypt_message=True)
    
    # Dimostra la query dei log
    print("\nQuery dei log:")
    logs = logger.query_logs(level="INFO", limit=10)
    for log in logs:
        print(f"{log['timestamp']} - {log['level']} - {log['message']}")
    
    # Dimostra l'esportazione dei log
    export_path = logger.export_logs_for_analysis(format="csv", level="INFO")
    print(f"\nLog esportati in: {export_path}")
    
    # Dimostra l'archiviazione manuale (normalmente eseguita automaticamente)
    print("\nArchiviazione manuale dei log:")
    logger.archive_old_logs()
    
    # Ferma lo scheduler prima di uscire
    logger.stop()
    
    return logger

if __name__ == "__main__":
    test_enhanced_db_logger() 