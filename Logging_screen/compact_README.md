# Sistema di Logging Compatto

Due approcci di logging Python ottimizzati per efficienza, sicurezza e conformità GDPR/HIPAA.

## Installazione

```bash
pip install -r compact_requirements.txt
```

## Approcci

### 1. Logger Basato su File (enhanced_method1_compact.py)
- Rotazione automatica dei file di log
- Eliminazione automatica dei log vecchi
- Crittografia dei messaggi sensibili
- Anonimizzazione dei dati personali
- Esportazione per analisi con opzione di decrittazione

### 2. Logger Basato su Database (enhanced_method2_compact.py)
- Archiviazione automatica in database separati
- Query avanzate con filtri multipli
- Crittografia dei messaggi sensibili
- Audit trail integrato per monitorare gli accessi
- Esportazione in CSV/JSON con opzione di decrittazione

## Caratteristiche Comuni
- Gestione automatica dell'archiviazione/eliminazione (40-50 log/giorno)
- Leggibilità e accessibilità per analisi
- Sicurezza GDPR/HIPAA (anonimizzazione, crittografia, controllo accessi)
- Formato strutturato (timestamp, livelli di gravità, identificatori, metadati)

## Utilizzo

```bash
python compact_main.py --method both
```

Opzioni: `file`, `db`, `both`, `compare`

### Esempi

```python
# Logger File
from enhanced_method1_compact import CompactFileLogger
logger = CompactFileLogger(log_dir="logs", max_size_mb=10, backup_count=5, retention_days=30)
logger.log("info", "Messaggio", user_id="user123", component="auth")
logger.log("error", "Dati sensibili", sensitive_data="4111-1111-1111-1111", encrypt=True)
logger.cleanup_old_logs()
logger.export_logs_for_analysis(decrypt=True)

# Logger Database
from enhanced_method2_compact import CompactDBLogger
logger = CompactDBLogger(db_path="logs.db", archive_days=30, retention_days=90)
logger.log("info", "Messaggio", user_id="user123", component="auth")
logger.log("error", "Dati sensibili", encrypt_message=True)
logs = logger.query_logs(level="INFO", decrypt=True)
logger.export_logs_for_analysis(format="csv", decrypt=True)
logger.stop() 