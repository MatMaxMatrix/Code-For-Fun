
import logging  # Import del modulo logging

# Configurazione di base del logging:
# - I log vengono salvati nel file "logs.txt".
# - Il livello minimo di log è INFO (INFO, WARNING ed ERROR saranno registrati).
# - Il formato del log include data/ora, livello di gravità e messaggio.
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_to_file(level, message):
    """
    Registra un messaggio di log con il livello specificato.
    
    :param level: Il livello di log (es. "info", "warning", "error").
    :param message: Il messaggio da registrare.
    """
    
    # Ottiene la funzione di logging corrispondente al livello specificato
    log_function = getattr(logging, level.lower(), None)

    if callable(log_function):
        log_function(message)  # Registra il messaggio con il livello corretto
    else:
        # Se il livello non è valido, registra un errore predefinito
        logging.error(f"Tentativo di usare un livello di log non valido: {level}")