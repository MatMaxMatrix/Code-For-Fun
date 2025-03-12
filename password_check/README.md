# Sistema di Verifica Password

Questo sistema permette di verificare la sicurezza delle password utilizzando tre diversi metodi di analisi, ciascuno implementato come script standalone:

1. **Metodo Base**: verifica che la password abbia almeno 8 caratteri e contenga una varietà di caratteri (maiuscole, minuscole, numeri e simboli).
2. **Metodo Avanzato**: esegue i controlli del metodo base e verifica se la password è presente in una lista di credenziali compromesse.
3. **Metodo Euristico**: esegue i controlli del metodo avanzato e confronta la password con quelle comuni usando un'analisi di similarità.

## Struttura del Progetto

- `basic_method.py`: implementa il metodo base di verifica (completamente autonomo)
- `advanced_method.py`: implementa il metodo avanzato di verifica (completamente autonomo)
- `heuristic_method.py`: implementa il metodo euristico di verifica (completamente autonomo)

Ogni script è completamente indipendente e può essere eseguito senza dipendere dagli altri file.

## Come Usare

Puoi eseguire ciascun script individualmente:

```bash
python basic_method.py
python advanced_method.py
python heuristic_method.py
```

Ogni script:
1. Esegue automaticamente test su un set di password predefinite
2. Permette all'utente di inserire una propria password per verificarla

## Funzionalità

- Verifica della lunghezza minima della password
- Verifica della presenza di caratteri di diverso tipo
- Controllo contro una lista di password compromesse
- Analisi di similarità con password comuni
- Suggerimenti personalizzati per migliorare la sicurezza della password

## Differenze tra i Metodi

- **Metodo Base**: controlli essenziali (lunghezza e varietà di caratteri)
- **Metodo Avanzato**: aggiunge il controllo contro una lista di password compromesse
- **Metodo Euristico**: aggiunge l'analisi di similarità per identificare password simili a quelle compromesse 