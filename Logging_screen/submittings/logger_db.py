import sqlite3, datetime, os, uuid, hashlib, json, logging, threading, time
from cryptography.fernet import Fernet

# Configurazione globale
DB_PATH, ARCHIVE_DIR = "logs_db.db", "archivi_log"
GIORNI_ARCHIVIAZIONE, GIORNI_CONSERVAZIONE = 30, 90
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Gestione chiave di crittografia
def get_cipher():
    """Ottiene o crea una chiave di crittografia."""
    key_dir, key_file = os.path.dirname(DB_PATH) or ".", os.path.join(os.path.dirname(DB_PATH) or ".", ".db_key")
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f: key = f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f: f.write(key)
    return Fernet(key)

CIPHER = get_cipher()

# Inizializza il database
def init_database():
    """Inizializza la struttura del database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, log_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL, level TEXT NOT NULL, component TEXT NOT NULL,
                    user_id_hash TEXT, message TEXT NOT NULL, encrypted INTEGER DEFAULT 0,
                    metadata TEXT
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs (timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_level ON logs (level)")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accessi_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
                    utente TEXT NOT NULL, azione TEXT NOT NULL, dettagli TEXT
                )
            """)
            conn.commit()
    except sqlite3.Error as e: logging.error(f"Errore database: {e}")

init_database()

# Thread di manutenzione
stop_thread = False
def maintenance_worker():
    """Thread di manutenzione che esegue archiviazione e pulizia periodica."""
    while not stop_thread:
        try:
            if 'archive_old_logs' in globals(): archive_old_logs()
            if 'cleanup_archived_logs' in globals(): cleanup_archived_logs()
        except Exception as e: logging.error(f"Errore manutenzione: {e}")
        for _ in range(86400):  # 24 ore
            if stop_thread: break
            time.sleep(1)

maintenance_thread = threading.Thread(target=maintenance_worker)
maintenance_thread.daemon = True
maintenance_thread.start()

def log_message(level, message, user_id=None, component="generale", sensitive_data=None, additional_data=None, encrypt_message=False):
    """Registra un messaggio di log nel database con metadati avanzati."""
    try:
        log_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        user_id_hash = hashlib.sha256(str(user_id).encode()).hexdigest() if user_id else None
        
        # Prepara metadati
        metadata = {}
        if additional_data: metadata.update(additional_data)
        if sensitive_data: metadata["hash_dati_sensibili"] = hashlib.sha256(str(sensitive_data).encode()).hexdigest()
        metadata_json = json.dumps(metadata) if metadata else None
        
        # Cripta messaggio se richiesto
        if encrypt_message: message = CIPHER.encrypt(message.encode()).decode()
        
        # Inserisci log
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO logs (log_id, timestamp, level, component, user_id_hash, message, encrypted, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (log_id, timestamp, level.upper(), component, user_id_hash, message, encrypt_message, metadata_json)
            )
        return log_id
    except sqlite3.Error as e:
        logging.error(f"Errore logging: {e}")
        return None

def log_access(utente, azione, dettagli=None):
    """Registra un accesso o un'operazione sui log per l'audit trail."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO accessi_log (timestamp, utente, azione, dettagli) VALUES (?, ?, ?, ?)",
                (datetime.datetime.now().isoformat(), utente, azione, dettagli)
            )
    except sqlite3.Error as e: logging.error(f"Errore audit: {e}")

def archive_old_logs():
    """Archivia i log più vecchi dell'intervallo configurato in un database separato."""
    try:
        # Calcola soglia e nome archivio
        archive_threshold = datetime.datetime.now() - datetime.timedelta(days=GIORNI_ARCHIVIAZIONE)
        archive_threshold_str = archive_threshold.isoformat()
        archive_file = os.path.join(ARCHIVE_DIR, f"archivio_log_{datetime.datetime.now().strftime('%Y%m%d')}.db")
        
        with sqlite3.connect(DB_PATH) as conn:
            # Verifica se ci sono log da archiviare
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM logs WHERE timestamp <= ?", (archive_threshold_str,))
            count = cursor.fetchone()[0]
            if count == 0: return
            
            # Crea database di archivio
            with sqlite3.connect(archive_file) as archive_conn:
                conn.backup(archive_conn)
                archive_conn.execute("DELETE FROM logs WHERE timestamp > ?", (archive_threshold_str,))
                conn.execute("DELETE FROM logs WHERE timestamp <= ?", (archive_threshold_str,))
                
            # Registra operazione
            log_access("SISTEMA", "ARCHIVIAZIONE", f"Archiviati {count} log in {archive_file}")
            print(f"Archiviati {count} log in {archive_file}")
    except Exception as e: logging.error(f"Errore archiviazione: {e}")

def cleanup_archived_logs():
    """Elimina gli archivi di log più vecchi del periodo di conservazione configurato."""
    try:
        retention_threshold = datetime.datetime.now() - datetime.timedelta(days=GIORNI_CONSERVAZIONE)
        for filename in os.listdir(ARCHIVE_DIR):
            if not filename.startswith("archivio_log_"): continue
            file_path = os.path.join(ARCHIVE_DIR, filename)
            try:
                date_str = filename.replace("archivio_log_", "").replace(".db", "")
                file_date = datetime.datetime.strptime(date_str, "%Y%m%d")
                if file_date < retention_threshold:
                    os.remove(file_path)
                    log_access("SISTEMA", "ELIMINAZIONE", f"Eliminato archivio {filename}")
                    print(f"Archivio eliminato: {filename}")
            except (ValueError, OSError) as e: logging.error(f"Errore pulizia: {e}")
    except Exception as e: logging.error(f"Errore pulizia archivi: {e}")

def query_logs(data_inizio=None, data_fine=None, level=None, component=None, user_id=None, limit=100, decrypt=False):
    """Esegue una query sui log con vari filtri."""
    try:
        # Costruisci query
        query, params = "SELECT * FROM logs WHERE 1=1", []
        if data_inizio:
            query += " AND timestamp >= ?"
            params.append(datetime.datetime.strptime(data_inizio, "%Y-%m-%d").isoformat())
        if data_fine:
            query += " AND timestamp < ?"
            params.append((datetime.datetime.strptime(data_fine, "%Y-%m-%d") + datetime.timedelta(days=1)).isoformat())
        if level: query, params = query + " AND level = ?", params + [level.upper()]
        if component: query, params = query + " AND component = ?", params + [component]
        if user_id: query, params = query + " AND user_id_hash = ?", params + [hashlib.sha256(str(user_id).encode()).hexdigest()]
        
        # Ordina e limita
        query, params = query + " ORDER BY timestamp DESC LIMIT ?", params + [limit]
        
        # Esegui query
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()
            
            # Registra accesso
            log_access("API", "QUERY", f"Query con filtri: {json.dumps({'inizio': data_inizio, 'fine': data_fine, 'livello': level})}")
            
            # Processa risultati
            results = []
            for row in rows:
                log_entry = dict(row)
                if decrypt and log_entry.get("encrypted"):
                    try: log_entry["message"] = CIPHER.decrypt(log_entry["message"].encode()).decode()
                    except Exception: log_entry["message"] = "[Messaggio criptato]"
                if log_entry.get("metadata"): log_entry["metadata"] = json.loads(log_entry["metadata"])
                results.append(log_entry)
            return results
    except Exception as e:
        logging.error(f"Errore query: {e}")
        return []

def export_logs(output_file=None, format="csv", decrypt=False, **query_params):
    """Esporta i log in un formato adatto all'analisi."""
    # Ottieni log
    logs = query_logs(decrypt=decrypt, **query_params)
    if not logs: 
        print("Nessun log da esportare")
        return None
    
    # Nome file
    output_file = output_file or f"esportazione_log_{datetime.datetime.now().strftime('%Y-%m-%d')}.{format}"
    
    try:
        if format.lower() == "csv":
            import csv
            # Prepara i dati per l'esportazione
            export_data, all_fields = [], set()
            for log in logs:
                log_dict = {}
                for key in log.keys():
                    if key == 'metadata':
                        metadata = log[key]
                        if isinstance(metadata, dict):
                            for meta_key, meta_value in metadata.items():
                                meta_field = f"metadata_{meta_key}"
                                log_dict[meta_field] = meta_value
                                all_fields.add(meta_field)
                    else:
                        log_dict[key] = log[key]
                        all_fields.add(key)
                export_data.append(log_dict)
            
            # Scrivi CSV
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=sorted(all_fields))
                writer.writeheader()
                for row in export_data: writer.writerow(row)
        
        elif format.lower() == "json":
            with open(output_file, 'w') as jsonfile: json.dump(logs, jsonfile, indent=2)
        else:
            raise ValueError(f"Formato non supportato: {format}")
        
        # Registra esportazione
        log_access("API", "ESPORTAZIONE", f"Esportati {len(logs)} log in {output_file}")
        print(f"Esportati {len(logs)} log in {output_file}")
        return output_file
    except Exception as e:
        logging.error(f"Errore esportazione: {e}")
        return None

def stop_maintenance():
    """Ferma il thread di manutenzione."""
    global stop_thread
    stop_thread = True
    if maintenance_thread.is_alive(): maintenance_thread.join(timeout=1) 