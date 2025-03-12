import argparse
from enhanced_method1_compact import CompactFileLogger
from enhanced_method2_compact import CompactDBLogger

def demo_file_logger():
    """Dimostra il logger basato su file."""
    print("\n=== LOGGER BASATO SU FILE ===")
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
    
    # Esporta log normali
    export_path = logger.export_logs_for_analysis(level="info")
    print(f"Log esportati in: {export_path}")
    
    # Esporta con decrittazione
    secure_export_path = logger.export_logs_for_analysis(decrypt=True)
    print(f"Log decriptati esportati in: {secure_export_path}")
    
    return logger

def demo_db_logger():
    """Dimostra il logger basato su database."""
    print("\n=== LOGGER BASATO SU DATABASE ===")
    logger = CompactDBLogger(db_path="compact_logs.db", archive_days=30, retention_days=90)
    
    # Log di esempio
    logger.log("info", "Applicazione avviata", component="system")
    logger.log("info", "Login utente", user_id="user123", component="auth")
    logger.log("warning", "Tentativo fallito", user_id="user456", component="auth", 
              additional_data={"ip": "192.168.1.1", "attempts": 3})
    
    # Log con dati sensibili
    logger.log("error", "Dati carta di credito", user_id="user123", component="payment", 
              sensitive_data="4111-1111-1111-1111", additional_data={"amount": 99.99})
    
    # Log con messaggio criptato
    logger.log("critical", "Dati sensibili", user_id="admin", component="security", encrypt_message=True)
    
    # Query e export
    print("\nQuery dei log:")
    logs = logger.query_logs(level="INFO", limit=10)
    for log in logs:
        print(f"{log['timestamp']} - {log['level']} - {log['message']}")
    
    # Esporta log normali
    export_path = logger.export_logs_for_analysis(format="csv", level="INFO")
    print(f"Log esportati in: {export_path}")
    
    # Esporta log con decrittazione
    secure_export_path = logger.export_logs_for_analysis(format="csv", decrypt=True)
    print(f"Log decriptati esportati in: {secure_export_path}")
    
    # Manutenzione manuale
    logger.archive_old_logs()
    logger.stop()
    
    return logger

def compare_approaches():
    """Confronta i due approcci."""
    print("\n=== CONFRONTO APPROCCI ===")
    
    print("\nAPPROCCIO 1: FILE")
    print("Vantaggi: Semplicità, nessuna dipendenza da DB, facile ispezione manuale")
    print("Svantaggi: Meno efficiente per query complesse, meno scalabile")
    
    print("\nAPPROCCIO 2: DATABASE")
    print("Vantaggi: Query avanzate, struttura flessibile, audit trail, scalabilità")
    print("Svantaggi: Maggiore complessità, dipendenza da DB")
    
    print("\nENTRAMBI IMPLEMENTANO:")
    print("- Archiviazione/eliminazione automatica")
    print("- Leggibilità e accessibilità per analisi")
    print("- Sicurezza (GDPR/HIPAA): anonimizzazione, crittografia, controllo accessi")
    print("- Formato strutturato: timestamp, livelli, ID, metadati")

def main():
    """Funzione principale."""
    parser = argparse.ArgumentParser(description="Demo sistemi di logging compatti")
    parser.add_argument("--method", choices=["file", "db", "both", "compare"], 
                       default="both", help="Metodo da dimostrare")
    args = parser.parse_args()
    
    if args.method == "file" or args.method == "both":
        demo_file_logger()
    
    if args.method == "db" or args.method == "both":
        demo_db_logger()
    
    if args.method == "compare" or args.method == "both":
        compare_approaches()
    
    print("\nDemo completata!")

if __name__ == "__main__":
    main() 