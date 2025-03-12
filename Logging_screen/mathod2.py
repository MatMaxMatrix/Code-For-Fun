import logging
import sqlite3
import datetime

# Funzione per registrare un log nel database SQLite
def log_to_db(level, message):
    """
    Registra un messaggio di log nel database SQLite.

    :param level: Il livello del log (es. "INFO", "WARNING", "ERROR").
    :param message: Il messaggio da salvare nel database.
    """
    try:
        # Connessione al database SQLite
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

            # La commit avviene automaticamente con `with`

    except sqlite3.Error as e:
        # Logga l'errore nel file di log in caso di problemi con il database
        logging.error(f"Errore nel logging su database: {e}")
