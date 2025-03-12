
import logging
import sqlite3
import datetime
import os

# Configurazione di base del logging su file
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_to_file(level, message):
    """
    Registra un messaggio di log nel file di testo.

    :param level: Il livello di log (es. "info", "warning", "error").
    :param message: Il messaggio da registrare.
    """
    log_function = getattr(logging, level.lower(), None)
    if callable(log_function):
        log_function(message)
    else:
        logging.error(f"Tentativo di usare un livello di log non valido: {level}")

def log_to_db(level, message):
    """
    Registra un messaggio di log nel database SQLite.

    :param level: Il livello del log (es. "INFO", "WARNING", "ERROR").
    :param message: Il messaggio da salvare nel database.
    """
    try:
        with sqlite3.connect("logs.db") as conn:
            cursor = conn.cursor()

            # Creazione della tabella logs se non esiste già
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            """)

            # Generazione del timestamp corrente
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Inserimento del log nel database
            cursor.execute("INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)", 
                           (timestamp, level, message))
    except sqlite3.Error as e:
        logging.error(f"Errore nel logging su database: {e}")

def test_logging():
    """Esegue un test registrando log su file e database, poi verifica la scrittura."""
    print("Eseguendo test di logging...")

    # Messaggi di test
    log_to_file("info", "Test log su file - Info")
    log_to_file("warning", "Test log su file - Warning")
    log_to_file("error", "Test log su file - Error")

    log_to_db("info", "Test log su database - Info")
    log_to_db("warning", "Test log su database - Warning")
    log_to_db("error", "Test log su database - Error")

    # Verifica che il file di log esista
    if os.path.exists("logs.txt"):
        print("Il file logs.txt è stato creato correttamente.")
    else:
        print("Errore: logs.txt non trovato.")

    # Verifica che i log siano stati scritti nel database
    try:
        with sqlite3.connect("logs.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM logs")
            count = cursor.fetchone()[0]

            if count > 0:
                print(f"{count} log trovati nel database.")
            else:
                print("Nessun log trovato nel database.")
    except sqlite3.Error as e:
        print(f"Errore durante il controllo del database: {e}")

# Esegue il test
if __name__ == "__main__":
    test_logging()

