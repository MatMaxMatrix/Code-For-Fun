# Image Analysis Chatbot

Un'applicazione di chatbot per l'analisi di immagini utilizzando l'API di OpenAI.

## Funzionalità

- Interfaccia grafica con area per la selezione dell'immagine, miniatura, chat a bolle e campo di input
- Gestione dell'immagine: consente all'utente di selezionare un'immagine (formati png, jpg, jpeg) e visualizza una miniatura
- Interazione con il modello di IA: invia il testo e, se disponibile, l'immagine codificata in base64 alle API remote
- Elaborazione della risposta: riceve e formatta il testo di risposta per una visualizzazione corretta
- Gestione degli errori: controlla input mancanti ed errori nella chiamata alle API

## Requisiti

- Python 3.6+
- tkinter (incluso nella maggior parte delle installazioni Python)
- PIL (Pillow)
- openai (per la modalità reale)
- tkinterdnd2 (opzionale, per il supporto drag & drop)

## Installazione

```bash
pip install pillow openai
pip install tkinterdnd2  # Opzionale, per il supporto drag & drop
```

## Utilizzo

### Modalità Demo (Dummy)

Per eseguire l'applicazione in modalità demo (senza chiamate API reali):

```bash
python image_analysis_chatbot.py
```

### Modalità Reale (con OpenAI API)

Per utilizzare l'API di OpenAI, è necessario impostare la chiave API come variabile d'ambiente:

```bash
# Linux/macOS
export OPENAI_API_KEY="your-api-key-here"
export USE_REAL_MODEL=1
python image_analysis_chatbot.py

# Windows
set OPENAI_API_KEY=your-api-key-here
set USE_REAL_MODEL=1
python image_analysis_chatbot.py
```

In alternativa, è possibile modificare il file `real_model_integration.py` e inserire direttamente la chiave API.

## Struttura del Progetto

- `image_analysis_chatbot.py`: Contiene la classe principale `ImageAnalysisChatBot` che gestisce l'interfaccia utente e la logica dell'applicazione
- `real_model_integration.py`: Contiene la funzione `real_model` che interagisce con l'API di OpenAI

## Note

- L'applicazione supporta il drag & drop delle immagini se la libreria `tkinterdnd2` è installata
- In modalità demo, l'applicazione restituisce risposte predefinite senza chiamare API esterne
- In modalità reale, l'applicazione utilizza il modello GPT-4 Vision di OpenAI per analizzare le immagini 