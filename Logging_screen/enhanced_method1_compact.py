import logging
import logging.handlers
import os
import datetime
import hashlib
import uuid
from cryptography.fernet import Fernet
import json

class CompactFileLogger:
    """Sistema di logging compatto basato su file con rotazione automatica e conformità GDPR/HIPAA."""
    
    def __init__(self, log_dir="logs", max_size_mb=10, backup_count=5, retention_days=30):
        """Inizializza il logger compatto basato su file."""
        # Setup base
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "app.log")
        self.retention_days = retention_days
        
        # Crittografia - genera una chiave e salva in un file
        key_file = os.path.join(log_dir, ".key")
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)
        
        # Configurazione logger
        self.logger = logging.getLogger("compact_file_logger")
        self.logger.setLevel(logging.INFO)
        
        # Handler con rotazione
        handler = logging.handlers.RotatingFileHandler(
            self.log_file, maxBytes=max_size_mb * 1024 * 1024, backupCount=backup_count
        )
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(log_id)s - %(user_id)s - %(component)s - %(message)s"
        ))
        self.logger.addHandler(handler)
    
    def log(self, level, message, user_id=None, component="general", sensitive_data=None, additional_data=None, encrypt=False):
        """Registra un messaggio di log con metadati avanzati."""
        # Genera ID e hash dati sensibili
        log_id = str(uuid.uuid4())
        hashed_user_id = hashlib.sha256(str(user_id).encode()).hexdigest() if user_id else "N/A"
        
        # Prepara metadati
        extra_data = {}
        if additional_data:
            extra_data.update(additional_data)
        if sensitive_data:
            extra_data["sensitive_data_hash"] = hashlib.sha256(str(sensitive_data).encode()).hexdigest()
        
        # Crea messaggio completo
        full_message = message
        if extra_data:
            full_message += f" | {json.dumps(extra_data)}"
        
        # Cripta il messaggio se richiesto
        if encrypt:
            full_message = f"ENCRYPTED:{self.cipher.encrypt(full_message.encode()).decode()}"
        
        # Log con extra
        extra = {"log_id": log_id, "user_id": hashed_user_id, "component": component}
        log_function = getattr(self.logger, level.lower(), None)
        if callable(log_function):
            log_function(full_message, extra=extra)
        else:
            self.logger.error(f"Livello di log non valido: {level}", extra=extra)
    
    def decrypt_message(self, encrypted_message):
        """Decripta un messaggio criptato."""
        if encrypted_message.startswith("ENCRYPTED:"):
            try:
                return self.cipher.decrypt(encrypted_message[10:].encode()).decode()
            except Exception:
                return "[Errore di decrittazione]"
        return encrypted_message
    
    def cleanup_old_logs(self):
        """Elimina i file di log più vecchi della retention_days configurata."""
        threshold = datetime.datetime.now() - datetime.timedelta(days=self.retention_days)
        
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            if os.path.isdir(file_path) or filename == ".key":
                continue
                
            if filename.startswith("app.log.") or filename == "app.log":
                file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mod_time < threshold:
                    try:
                        os.remove(file_path)
                        print(f"File di log eliminato: {filename}")
                    except Exception as e:
                        print(f"Errore durante l'eliminazione: {e}")
    
    def export_logs_for_analysis(self, output_file=None, start_date=None, end_date=None, level=None, component=None, decrypt=False):
        """Esporta i log in formato CSV per analisi."""
        import csv
        from datetime import datetime
        
        # Nome file di default
        if not output_file:
            today = datetime.now().strftime("%Y-%m-%d")
            output_file = f"logs_export_{today}.csv"
        
        # Converti date
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        
        # Intestazione CSV
        headers = ["Timestamp", "Level", "Log ID", "User ID", "Component", "Message", "Extra Data"]
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            # Processa tutti i file di log
            for filename in sorted(os.listdir(self.log_dir)):
                if not (filename.startswith("app.log") and os.path.isfile(os.path.join(self.log_dir, filename))):
                    continue
                    
                with open(os.path.join(self.log_dir, filename), 'r') as logfile:
                    for line in logfile:
                        try:
                            # Estrai componenti
                            parts = line.strip().split(" - ", 5)
                            if len(parts) < 6:
                                continue
                                
                            timestamp_str, log_level, log_id, user_id, component_name, message = parts
                            
                            # Applica filtri
                            log_dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                            if (start_dt and log_dt < start_dt) or (end_dt and log_dt > end_dt) or \
                               (level and log_level.lower() != level.lower()) or \
                               (component and component_name.lower() != component.lower()):
                                continue
                            
                            # Decripta se necessario
                            if decrypt and message.startswith("ENCRYPTED:"):
                                message = self.decrypt_message(message)
                                
                            # Estrai dati extra
                            extra_data = ""
                            if " | " in message and not message.startswith("ENCRYPTED:"):
                                message, extra_data = message.split(" | ", 1)
                                
                            # Scrivi riga
                            writer.writerow([timestamp_str, log_level, log_id, user_id, component_name, message, extra_data])
                        except Exception as e:
                            print(f"Errore elaborazione log: {e}")
        
        return output_file

def test_compact_file_logger():
    """Test del logger compatto."""
    logger = CompactFileLogger(log_dir="compact_logs_file", max_size_mb=1, backup_count=5, retention_days=30)
    
    # Log di esempio
    logger.log("info", "Applicazione avviata", component="system")
    logger.log("info", "Login utente", user_id="user123", component="auth")
    logger.log("warning", "Tentativo fallito", user_id="user456", component="auth", 
              additional_data={"ip": "192.168.1.1", "attempts": 3})
    
    # Log con dati sensibili (criptato)
    logger.log("error", "Dati carta di credito", user_id="user123", component="payment", 
              sensitive_data="4111-1111-1111-1111", additional_data={"amount": 99.99}, encrypt=True)
    
    # Manutenzione
    logger.cleanup_old_logs()
    export_path = logger.export_logs_for_analysis(level="info")
    print(f"Log esportati in: {export_path}")
    
    # Esporta con decrittazione
    secure_export_path = logger.export_logs_for_analysis(decrypt=True)
    print(f"Log decriptati esportati in: {secure_export_path}")
    
    return logger

if __name__ == "__main__":
    test_compact_file_logger() 