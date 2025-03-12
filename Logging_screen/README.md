# Sistema di Logging Avanzato

Questo progetto implementa due approcci avanzati per il logging in Python, progettati per soddisfare requisiti di efficienza, sicurezza e conformità.

## Requisiti

- Python 3.7+
- Dipendenze elencate in `requirements.txt`

## Installazione

```bash
pip install -r requirements.txt
```

## Approcci Implementati

### 1. Logger Basato su File (enhanced_method1.py)

Un sistema di logging che utilizza file di testo con rotazione automatica e funzionalità avanzate:

- **Rotazione automatica** dei file di log basata su dimensione
- **Eliminazione automatica** dei log vecchi
- **Crittografia** dei dati sensibili
- **Anonimizzazione** degli identificatori utente
- **Esportazione** dei log in formato CSV per analisi
- **Struttura avanzata** con ID univoci, componenti e metadati

### 2. Logger Basato su Database (enhanced_method2.py)

Un sistema di logging che utilizza SQLite con funzionalità avanzate:

- **Archiviazione automatica** dei log vecchi in database separati
- **Eliminazione automatica** degli archivi obsoleti
- **Query avanzate** con filtri multipli
- **Crittografia** dei messaggi sensibili
- **Audit trail** per monitorare gli accessi ai log
- **Esportazione** in formati CSV e JSON per analisi

## Caratteristiche Comuni

Entrambi gli approcci implementano:

1. **Gestione automatica dell'archiviazione/eliminazione** dei log vecchi
2. **Miglioramento della leggibilità e accessibilità** per analisi
3. **Sicurezza e conformità GDPR/HIPAA**:
   - Anonimizzazione dei dati personali
   - Crittografia dei dati sensibili
   - Politiche di conservazione dei dati
   - Controllo degli accessi
4. **Formato e struttura avanzati** dei log:
   - Timestamp precisi
   - Livelli di gravità
   - Identificatori univoci
   - Metadati strutturati

## Utilizzo

### Esecuzione della Demo

```bash
python enhanced_main.py --method both
```

Opzioni disponibili:
- `file`: Dimostra solo il logger basato su file
- `db`: Dimostra solo il logger basato su database
- `both`: Dimostra entrambi gli approcci (default)
- `compare`: Mostra solo il confronto tra i due approcci

### Esempi di Codice

#### Logger Basato su File

```python
from enhanced_method1 import EnhancedFileLogger

# Inizializza il logger
logger = EnhancedFileLogger(log_dir="logs", max_size_mb=10, backup_count=30, retention_days=90)

# Registra un log semplice
logger.log("info", "Applicazione avviata", component="system")

# Registra un log con dati utente (anonimizzati automaticamente)
logger.log("info", "Utente ha effettuato l'accesso", user_id="user123", component="auth")

# Registra un log con dati sensibili (hashati automaticamente)
logger.log("error", "Errore durante l'elaborazione del pagamento", 
          user_id="user123", component="payment", 
          sensitive_data="4111-1111-1111-1111", 
          additional_data={"amount": 99.99, "currency": "EUR"})

# Esporta i log per l'analisi
export_path = logger.export_logs_for_analysis(level="info")

# Pulisci i log vecchi
logger.cleanup_old_logs()
```

#### Logger Basato su Database

```python
from enhanced_method2 import EnhancedDBLogger

# Inizializza il logger
logger = EnhancedDBLogger(db_path="logs.db", archive_interval_days=30, retention_days=90)

# Registra un log semplice
logger.log("info", "Applicazione avviata", component="system")

# Registra un log con dati utente (anonimizzati automaticamente)
logger.log("info", "Utente ha effettuato l'accesso", user_id="user123", component="auth")

# Registra un log con dati sensibili (hashati automaticamente)
logger.log("error", "Errore durante l'elaborazione del pagamento", 
          user_id="user123", component="payment", 
          sensitive_data="4111-1111-1111-1111", 
          additional_data={"amount": 99.99, "currency": "EUR"})

# Registra un log con messaggio criptato
logger.log("critical", "Informazioni molto sensibili", 
          user_id="admin", component="security", 
          encrypt_message=True)

# Esegui una query sui log
logs = logger.query_logs(level="INFO", limit=10)

# Esporta i log per l'analisi
export_path = logger.export_logs_for_analysis(format="csv", level="INFO")

# Archivia manualmente i log vecchi (normalmente automatico)
logger.archive_old_logs()

# Ferma lo scheduler prima di uscire
logger.stop()
```

## Scelta dell'Approccio

- **Logger Basato su File**: Ideale per applicazioni più semplici, con volumi di log moderati e quando è importante la facilità di implementazione.

- **Logger Basato su Database**: Preferibile per applicazioni complesse, con necessità di query avanzate, analisi dettagliate e volumi di log elevati.

## Licenza

MIT 