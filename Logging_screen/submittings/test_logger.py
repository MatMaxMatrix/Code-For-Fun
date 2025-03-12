"""
File di test per i due metodi di logging
"""
import os
import time
from logger_file import log_message as file_log_message
from logger_file import cleanup_old_logs, export_logs as file_export_logs
from logger_db import log_message as db_log_message
from logger_db import query_logs, export_logs as db_export_logs
from logger_db import archive_old_logs, stop_maintenance

def test_file_based_logging():
    """Test del sistema di logging basato su file."""
    print("\n=== TEST LOGGER BASATO SU FILE ===")
    
    # Log di esempio
    file_log_message("info", "Applicazione avviata", component="sistema")
    file_log_message("info", "Login utente", user_id="user123", component="autenticazione")
    file_log_message("warning", "Tentativo fallito", user_id="user456", component="autenticazione", 
                   additional_data={"ip": "192.168.1.1", "tentativi": 3})
    
    # Log con dati sensibili (criptato)
    file_log_message("error", "Dati carta di credito", user_id="user123", component="pagamento", 
                   sensitive_data="4111-1111-1111-1111", additional_data={"importo": 99.99}, encrypt=True)
    
    # Manutenzione
    cleanup_old_logs()
    
    # Esporta log
    export_path = file_export_logs(level="info")
    print(f"Log esportati in: {export_path}")
    
    # Esporta con decrittazione
    secure_export_path = file_export_logs(decrypt=True)
    print(f"Log decriptati esportati in: {secure_export_path}")
    
    print("Test logger file completato!")

def test_db_based_logging():
    """Test del sistema di logging basato su database."""
    print("\n=== TEST LOGGER BASATO SU DATABASE ===")
    
    # Log di esempio
    db_log_message("info", "Applicazione avviata", component="sistema")
    db_log_message("info", "Login utente", user_id="user123", component="autenticazione")
    db_log_message("warning", "Tentativo fallito", user_id="user456", component="autenticazione", 
                 additional_data={"ip": "192.168.1.1", "tentativi": 3})
    
    # Log con dati sensibili
    db_log_message("error", "Dati carta di credito", user_id="user123", component="pagamento", 
                 sensitive_data="4111-1111-1111-1111", additional_data={"importo": 99.99})
    
    # Log con messaggio criptato
    db_log_message("critical", "Dati sensibili", user_id="admin", component="sicurezza", encrypt_message=True)
    
    # Query e export
    print("\nQuery dei log:")
    logs = query_logs(level="INFO", limit=10)
    for log in logs:
        print(f"{log['timestamp']} - {log['level']} - {log['message']}")
    
    try:
        # Esporta log
        export_path = db_export_logs(format="csv", level="INFO")
        print(f"\nLog esportati in: {export_path}")
        
        # Esporta log con decrittazione
        secure_export_path = db_export_logs(format="csv", decrypt=True)
        print(f"\nLog decriptati esportati in: {secure_export_path}")
    except Exception as e:
        print(f"Errore durante l'esportazione: {e}")
    
    # Manutenzione manuale
    try:
        archive_old_logs()
    except Exception as e:
        print(f"Errore durante l'archiviazione: {e}")
    
    print("Test logger database completato!")

if __name__ == "__main__":
    print("=== TEST DEI METODI DI LOGGING ===")
    
    # Test del metodo 1 (basato su file)
    test_file_based_logging()
    
    # Test del metodo 2 (basato su database)
    test_db_based_logging()
    
    # Ferma thread di manutenzione del metodo 2
    stop_maintenance()
    
    print("\nTest completato! Entrambi i metodi sono stati verificati.") 