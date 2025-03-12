import logging, logging.handlers, os, datetime, hashlib, uuid, json
from cryptography.fernet import Fernet

# Configurazione globale
LOG_DIR, LOG_FILE = "logs_file", os.path.join("logs_file", "app.log")
MAX_SIZE_MB, BACKUP_COUNT, RETENTION_DAYS = 5, 3, 30
os.makedirs(LOG_DIR, exist_ok=True)

# Gestione chiave di crittografia e inizializzazione logger
def get_cipher():
    """Ottiene o crea una chiave di crittografia."""
    key_file = os.path.join(LOG_DIR, ".key")
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f: key = f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f: f.write(key)
    return Fernet(key)

CIPHER = get_cipher()
logger = logging.getLogger("file_logger")
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=MAX_SIZE_MB * 1024 * 1024, backupCount=BACKUP_COUNT)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(log_id)s - %(user_id)s - %(component)s - %(message)s"))
logger.addHandler(handler)

def log_message(level, message, user_id=None, component="generale", sensitive_data=None, additional_data=None, encrypt=False):
    """Registra un messaggio di log con metadati avanzati."""
    log_id = str(uuid.uuid4())
    hashed_user_id = hashlib.sha256(str(user_id).encode()).hexdigest() if user_id else "N/A"
    
    # Prepara metadati e messaggio
    extra_data = {}
    if additional_data: extra_data.update(additional_data)
    if sensitive_data: extra_data["hash_dati_sensibili"] = hashlib.sha256(str(sensitive_data).encode()).hexdigest()
    
    full_message = message
    if extra_data: full_message += f" | {json.dumps(extra_data)}"
    if encrypt: full_message = f"CRITTOGRAFATO:{CIPHER.encrypt(full_message.encode()).decode()}"
    
    # Log con extra
    extra = {"log_id": log_id, "user_id": hashed_user_id, "component": component}
    log_function = getattr(logger, level.lower(), None)
    if callable(log_function): log_function(full_message, extra=extra)
    else: logger.error(f"Livello di log non valido: {level}", extra=extra)
    
    return log_id

def decrypt_message(encrypted_message):
    """Decripta un messaggio criptato."""
    if encrypted_message.startswith("CRITTOGRAFATO:"):
        try: return CIPHER.decrypt(encrypted_message[13:].encode()).decode()
        except Exception: return "[Errore di decrittazione]"
    return encrypted_message

def cleanup_old_logs():
    """Elimina i file di log più vecchi della retention_days configurata."""
    threshold = datetime.datetime.now() - datetime.timedelta(days=RETENTION_DAYS)
    for filename in os.listdir(LOG_DIR):
        file_path = os.path.join(LOG_DIR, filename)
        if os.path.isdir(file_path) or filename == ".key": continue
        if filename.startswith("app.log.") or filename == "app.log":
            if datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) < threshold:
                try: os.remove(file_path); print(f"File di log eliminato: {filename}")
                except Exception as e: print(f"Errore durante l'eliminazione: {e}")

def export_logs(output_file=None, start_date=None, end_date=None, level=None, component=None, decrypt=False):
    """Esporta i log in formato CSV per analisi."""
    import csv
    from datetime import datetime
    
    # Nome file e conversione date
    output_file = output_file or f"logs_export_{datetime.now().strftime('%Y-%m-%d')}.csv"
    start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Livello", "ID Log", "ID Utente", "Componente", "Messaggio", "Dati Extra"])
        
        for filename in sorted(os.listdir(LOG_DIR)):
            if not (filename.startswith("app.log") and os.path.isfile(os.path.join(LOG_DIR, filename))): continue
            with open(os.path.join(LOG_DIR, filename), 'r') as logfile:
                for line in logfile:
                    try:
                        parts = line.strip().split(" - ", 5)
                        if len(parts) < 6: continue
                        timestamp_str, log_level, log_id, user_id, component_name, message = parts
                        
                        # Applica filtri
                        log_dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                        if ((start_dt and log_dt < start_dt) or (end_dt and log_dt > end_dt) or
                            (level and log_level.lower() != level.lower()) or
                            (component and component_name.lower() != component.lower())): continue
                        
                        # Decripta e estrai dati extra
                        if decrypt and message.startswith("CRITTOGRAFATO:"): message = decrypt_message(message)
                        extra_data = ""
                        if " | " in message and not message.startswith("CRITTOGRAFATO:"):
                            message, extra_data = message.split(" | ", 1)
                            
                        writer.writerow([timestamp_str, log_level, log_id, user_id, component_name, message, extra_data])
                    except Exception as e: print(f"Errore elaborazione log: {e}")
    
    return output_file 