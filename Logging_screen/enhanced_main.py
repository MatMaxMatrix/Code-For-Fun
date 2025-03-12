import os
import time
import argparse
from enhanced_method1 import EnhancedFileLogger
from enhanced_method2 import EnhancedDBLogger

def demonstrate_file_logger():
    """Dimostra le funzionalità del logger avanzato basato su file."""
    print("\n=== DIMOSTRAZIONE LOGGER BASATO SU FILE ===")
    
    # Inizializza il logger
    logger = EnhancedFileLogger(log_dir="enhanced_logs_file", 
                               max_size_mb=1, 
                               backup_count=5, 
                               retention_days=30)
    
    # Registra alcuni log di esempio
    print("Registrazione di log di esempio...")
    logger.log("info", "Applicazione avviata", component="system")
    logger.log("info", "Utente ha effettuato l'accesso", user_id="user123", component="auth")
    logger.log("warning", "Tentativo di accesso fallito", user_id="user456", 
              component="auth", additional_data={"ip": "192.168.1.1", "attempts": 3})
    logger.log("error", "Errore durante l'elaborazione del pagamento", 
              user_id="user123", component="payment", 
              sensitive_data="4111-1111-1111-1111", 
              additional_data={"amount": 99.99, "currency": "EUR"})
    
    # Dimostra la pulizia dei log vecchi
    print("\nPulizia dei log vecchi...")
    logger.cleanup_old_logs()
    
    # Esporta i log per l'analisi
    print("\nEsportazione dei log per l'analisi...")
    export_path = logger.export_logs_for_analysis(level="info")
    print(f"Log esportati in: {export_path}")
    
    return logger

def demonstrate_db_logger():
    """Dimostra le funzionalità del logger avanzato basato su database."""
    print("\n=== DIMOSTRAZIONE LOGGER BASATO SU DATABASE ===")
    
    # Inizializza il logger
    logger = EnhancedDBLogger(db_path="enhanced_logs.db", 
                             archive_interval_days=30, 
                             retention_days=90)
    
    # Registra alcuni log di esempio
    print("Registrazione di log di esempio...")
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
    print("\nEsportazione dei log per l'analisi...")
    export_path = logger.export_logs_for_analysis(format="csv", level="INFO")
    print(f"Log esportati in: {export_path}")
    
    # Dimostra l'archiviazione manuale (normalmente eseguita automaticamente)
    print("\nArchiviazione manuale dei log...")
    logger.archive_old_logs()
    
    # Ferma lo scheduler prima di uscire
    logger.stop()
    
    return logger

def compare_approaches():
    """Confronta i due approcci di logging."""
    print("\n=== CONFRONTO TRA I DUE APPROCCI ===")
    
    print("\nAPPROCCIO 1: LOGGER BASATO SU FILE")
    print("Vantaggi:")
    print("- Semplicità di implementazione e utilizzo")
    print("- Nessuna dipendenza da database")
    print("- Rotazione automatica dei file di log")
    print("- Buona performance per volumi di log limitati")
    print("- Facile da ispezionare manualmente")
    
    print("\nSvantaggi:")
    print("- Meno efficiente per query complesse")
    print("- Limitazioni nella struttura dei dati")
    print("- Meno scalabile per grandi volumi di log")
    
    print("\nAPPROCCIO 2: LOGGER BASATO SU DATABASE")
    print("Vantaggi:")
    print("- Struttura dati più flessibile")
    print("- Query avanzate e filtri complessi")
    print("- Migliore per l'analisi dei dati")
    print("- Audit trail integrato")
    print("- Più scalabile per grandi volumi di log")
    
    print("\nSvantaggi:")
    print("- Maggiore complessità di implementazione")
    print("- Dipendenza da un database")
    print("- Potenzialmente più lento per operazioni di scrittura ad alto volume")
    
    print("\nCONFORMITÀ GDPR/HIPAA:")
    print("Entrambi gli approcci implementano:")
    print("- Anonimizzazione dei dati personali")
    print("- Crittografia per dati sensibili")
    print("- Politiche di conservazione dei dati")
    print("- Controllo degli accessi")
    print("- Audit trail")

def main():
    """Funzione principale che dimostra entrambi gli approcci di logging."""
    parser = argparse.ArgumentParser(description="Dimostrazione di sistemi di logging avanzati")
    parser.add_argument("--method", choices=["file", "db", "both", "compare"], 
                       default="both", help="Metodo di logging da dimostrare")
    args = parser.parse_args()
    
    if args.method == "file" or args.method == "both":
        file_logger = demonstrate_file_logger()
    
    if args.method == "db" or args.method == "both":
        db_logger = demonstrate_db_logger()
    
    if args.method == "compare" or args.method == "both":
        compare_approaches()
    
    print("\nDimostrazione completata!")

if __name__ == "__main__":
    main() 