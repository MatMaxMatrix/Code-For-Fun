import logging
import logging.handlers
import os
import datetime
import hashlib
import uuid
from cryptography.fernet import Fernet
import json
from functools import wraps

class EnhancedFileLogger:
    """
    Sistema di logging avanzato basato su file con rotazione automatica,
    conformità GDPR/HIPAA e struttura migliorata per l'analisi.
    """
    
    def __init__(self, log_dir="logs", max_size_mb=10, backup_count=30, 
                 retention_days=90, encryption_key=None):
        """
        Inizializza il logger avanzato basato su file.
        
        :param log_dir: Directory dove salvare i log
        :param max_size_mb: Dimensione massima di ogni file di log in MB
        :param backup_count: Numero di file di backup da mantenere
        :param retention_days: Giorni di conservazione dei log
        :param encryption_key: Chiave di crittografia (generata se None)
        """
        # Crea la directory dei log se non esiste
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Percorso del file di log
        self.log_file = os.path.join(log_dir, "application.log")
        
        # Configurazione della crittografia
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Configurazione del logger
        self.logger = logging.getLogger("enhanced_file_logger")
        self.logger.setLevel(logging.INFO)
        
        # Configurazione del formatter con campi aggiuntivi
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(log_id)s - %(user_id)s - "
            "%(component)s - %(message)s"
        )
        
        # Configurazione del RotatingFileHandler per la rotazione automatica
        handler = logging.handlers.RotatingFileHandler(
            self.log_file,
            maxBytes=max_size_mb * 1024 * 1024,  # Conversione in byte
            backupCount=backup_count
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Memorizza i parametri di configurazione
        self.retention_days = retention_days
        self.backup_count = backup_count
    
    def _generate_log_id(self):
        """Genera un ID univoco per il log."""
        return str(uuid.uuid4())
    
    def _hash_sensitive_data(self, data):
        """Applica l'hashing ai dati sensibili."""
        if not data:
            return "N/A"
        return hashlib.sha256(str(data).encode()).hexdigest()
    
    def _encrypt_message(self, message):
        """Cripta il messaggio di log."""
        return self.cipher.encrypt(message.encode()).decode()
    
    def _decrypt_message(self, encrypted_message):
        """Decripta il messaggio di log."""
        return self.cipher.decrypt(encrypted_message.encode()).decode()
    
    def log(self, level, message, user_id=None, component="general", 
            sensitive_data=None, additional_data=None):
        """
        Registra un messaggio di log con metadati avanzati.
        
        :param level: Livello di log (info, warning, error, critical)
        :param message: Messaggio principale del log
        :param user_id: ID dell'utente (opzionale, anonimizzato se presente)
        :param component: Componente del sistema che genera il log
        :param sensitive_data: Dati sensibili da proteggere (verranno hashati)
        :param additional_data: Dati aggiuntivi in formato dizionario
        """
        # Genera un ID univoco per il log
        log_id = self._generate_log_id()
        
        # Anonimizza l'ID utente se presente
        hashed_user_id = self._hash_sensitive_data(user_id) if user_id else "N/A"
        
        # Prepara i dati aggiuntivi
        extra_data = {}
        if additional_data:
            extra_data = additional_data
        
        # Aggiungi dati sensibili hashati se presenti
        if sensitive_data:
            extra_data["sensitive_data_hash"] = self._hash_sensitive_data(sensitive_data)
        
        # Crea il messaggio completo
        full_message = message
        if extra_data:
            # Aggiungi i dati extra come JSON
            full_message += f" | {json.dumps(extra_data)}"
        
        # Prepara gli extra per il logger
        extra = {
            "log_id": log_id,
            "user_id": hashed_user_id,
            "component": component
        }
        
        # Ottieni la funzione di logging corrispondente al livello
        log_function = getattr(self.logger, level.lower(), None)
        if callable(log_function):
            log_function(full_message, extra=extra)
        else:
            self.logger.error(f"Livello di log non valido: {level}", extra=extra)
    
    def cleanup_old_logs(self):
        """
        Elimina i file di log più vecchi della retention_days configurata.
        Questa funzione dovrebbe essere eseguita periodicamente.
        """
        current_time = datetime.datetime.now()
        retention_threshold = current_time - datetime.timedelta(days=self.retention_days)
        
        # Controlla tutti i file nella directory dei log
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)
            
            # Salta le directory
            if os.path.isdir(file_path):
                continue
                
            # Controlla se il file è un file di log
            if filename.startswith("application.log.") or filename == "application.log":
                # Ottieni la data di modifica del file
                file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                
                # Elimina il file se è più vecchio della soglia di conservazione
                if file_mod_time < retention_threshold:
                    try:
                        os.remove(file_path)
                        print(f"File di log eliminato: {filename}")
                    except Exception as e:
                        print(f"Errore durante l'eliminazione del file {filename}: {e}")
    
    def export_logs_for_analysis(self, output_file=None, start_date=None, end_date=None, 
                                level=None, component=None):
        """
        Esporta i log in un formato adatto all'analisi.
        
        :param output_file: File di output (default: logs_export_YYYY-MM-DD.csv)
        :param start_date: Data di inizio per il filtro (formato: YYYY-MM-DD)
        :param end_date: Data di fine per il filtro (formato: YYYY-MM-DD)
        :param level: Filtra per livello di log
        :param component: Filtra per componente
        :return: Percorso del file esportato
        """
        import csv
        from datetime import datetime
        
        # Nome file di default
        if not output_file:
            today = datetime.now().strftime("%Y-%m-%d")
            output_file = f"logs_export_{today}.csv"
        
        # Converti le date in oggetti datetime se specificate
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        
        # Prepara l'intestazione CSV
        headers = ["Timestamp", "Level", "Log ID", "User ID", "Component", "Message", "Extra Data"]
        
        # Apri il file di output
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            # Processa tutti i file di log
            for filename in sorted(os.listdir(self.log_dir)):
                if not (filename.startswith("application.log") and os.path.isfile(os.path.join(self.log_dir, filename))):
                    continue
                    
                file_path = os.path.join(self.log_dir, filename)
                
                # Leggi e processa ogni riga del file
                with open(file_path, 'r') as logfile:
                    for line in logfile:
                        try:
                            # Estrai i componenti del log
                            parts = line.strip().split(" - ", 5)
                            if len(parts) < 6:
                                continue
                                
                            timestamp_str, log_level, log_id, user_id, component_name, message = parts
                            
                            # Converti il timestamp
                            log_dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                            
                            # Applica i filtri
                            if start_dt and log_dt < start_dt:
                                continue
                            if end_dt and log_dt > end_dt:
                                continue
                            if level and log_level.lower() != level.lower():
                                continue
                            if component and component_name.lower() != component.lower():
                                continue
                                
                            # Estrai dati extra se presenti
                            extra_data = ""
                            if " | " in message:
                                message, extra_data = message.split(" | ", 1)
                                
                            # Scrivi la riga nel CSV
                            writer.writerow([
                                timestamp_str,
                                log_level,
                                log_id,
                                user_id,
                                component_name,
                                message,
                                extra_data
                            ])
                        except Exception as e:
                            print(f"Errore durante l'elaborazione della riga di log: {e}")
        
        return output_file

# Funzione di test per dimostrare l'uso del logger avanzato
def test_enhanced_file_logger():
    """Testa le funzionalità del logger avanzato basato su file."""
    # Inizializza il logger
    logger = EnhancedFileLogger(log_dir="enhanced_logs", max_size_mb=1, backup_count=5, retention_days=30)
    
    # Registra alcuni log di esempio
    logger.log("info", "Applicazione avviata", component="system")
    logger.log("info", "Utente ha effettuato l'accesso", user_id="user123", component="auth")
    logger.log("warning", "Tentativo di accesso fallito", user_id="user456", 
              component="auth", additional_data={"ip": "192.168.1.1", "attempts": 3})
    logger.log("error", "Errore durante l'elaborazione del pagamento", 
              user_id="user123", component="payment", 
              sensitive_data="4111-1111-1111-1111", 
              additional_data={"amount": 99.99, "currency": "EUR"})
    
    # Dimostra la pulizia dei log vecchi
    logger.cleanup_old_logs()
    
    # Esporta i log per l'analisi
    export_path = logger.export_logs_for_analysis(level="info")
    print(f"Log esportati in: {export_path}")
    
    return logger

if __name__ == "__main__":
    test_enhanced_file_logger() 