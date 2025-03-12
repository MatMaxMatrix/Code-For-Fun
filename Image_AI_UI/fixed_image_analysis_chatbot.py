#!/usr/bin/env python3
# fixed_image_analysis_chatbot.py - Fixed version of image_analysis_chatbot.py
import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import os
from PIL import Image, ImageTk

# Try to import tkinterdnd2, but handle errors properly
USE_DND = False
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    # Test if tkdnd is actually available
    test_root = tk.Tk()
    try:
        test_root.tk.call('package', 'require', 'tkdnd')
        USE_DND = True
    except tk.TclError:
        print("tkdnd Tcl package not available, disabling drag & drop support")
    finally:
        test_root.destroy()
except ImportError:
    print("tkinterdnd2 module not available, disabling drag & drop support")

# ------------------------------------------------------------------------------
class Response:
    """
    Classe base per le risposte del modello di IA.
    """
    message: str

    def __init__(self, message):
        self.message = message

# ------------------------------------------------------------------------------
class ImageAnalysisChatBot:
    """
    ChatBot per l'analisi di immagini.

    Funzionalità implementate:
    - Interfaccia grafica (punto 1): crea un'interfaccia con area per la selezione dell'immagine,
      miniatura, chat a bolle e campo di input.
    - Gestione dell'immagine (punto 2): consente all'utente di selezionare un'immagine (formati png, jpg, jpeg)
      e visualizza una miniatura.
    - Interazione con il modello di IA (punto 3): invia il testo e, se disponibile, l'immagine codificata in base64
      alle API remote.
    - Elaborazione della risposta (punto 4): riceve e formatta il testo di risposta per una visualizzazione corretta.
    - Gestione degli errori (punto 5): controlla input mancanti ed errori nella chiamata alle API.
    """
    def __init__(self, tk_root, chat_gpt_fn=None):
        self.root = tk_root
        self.root.title("ChatBot: Analisi Immagini")
        self.root.geometry("800x600")
        
        # Se non viene passata una funzione, si usa quella integrata (dummy)
        self._chat_gpt_fn = chat_gpt_fn if chat_gpt_fn is not None else self.dummy_chat_bot
        
        # Variabili per l'immagine
        self.image_path = ""
        self.image_base64 = ""
        self.image_loaded = False
        self.thumbnail = None
        
        # Costruzione dell'interfaccia grafica (punto 1)
        self.create_widgets()
        
    def create_widgets(self):
        # --- TOP: Selezione immagine e miniatura ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Pulsante per selezionare l'immagine
        self.select_btn = tk.Button(top_frame, text="Seleziona Immagine", command=self.select_image)
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        # Etichetta per mostrare il percorso dell'immagine selezionata
        self.path_label = tk.Label(top_frame, text="Nessuna immagine selezionata")
        self.path_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Frame per la miniatura dell'immagine
        self.thumbnail_frame = tk.Frame(self.root, width=200, height=200, bg="lightgray")
        self.thumbnail_frame.pack(side=tk.TOP, padx=10, pady=5)
        
        # Etichetta per la miniatura
        self.thumbnail_label = tk.Label(self.thumbnail_frame, text="L'immagine apparirà qui")
        self.thumbnail_label.pack(expand=True)
        
        # Configurazione del drag & drop se disponibile
        if USE_DND:
            try:
                self.thumbnail_label.drop_target_register(DND_FILES)
                self.thumbnail_label.dnd_bind('<<Drop>>', self.drop_image)
            except Exception as e:
                print(f"Error setting up drag & drop: {e}")
        
        # --- MIDDLE: Area chat ---
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Widget di testo per la chat
        self.chat_text = tk.Text(chat_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar per la chat
        scrollbar = tk.Scrollbar(chat_frame, command=self.chat_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_text.config(yscrollcommand=scrollbar.set)
        
        # --- BOTTOM: Area input ---
        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Entry per l'input dell'utente
        self.user_input = tk.Entry(input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.user_input.bind("<Return>", self.on_enter_pressed)
        
        # Pulsante di invio
        send_btn = tk.Button(input_frame, text="Invia", command=self.interactive_chat)
        send_btn.pack(side=tk.RIGHT, padx=5)
        
        # Aggiunta del messaggio iniziale
        self.add_message("Sistema", "Benvenuto nel ChatBot per l'analisi delle immagini! Seleziona un'immagine e inizia a chattare.")
    
    def select_image(self):
        """
        (Gestione dell'immagine - punto 2)
        Apre un dialogo per selezionare un'immagine e la carica.
        """
        file_path = filedialog.askopenfilename(
            title="Seleziona Immagine",
            filetypes=[("Immagini", "*.png *.jpg *.jpeg")]
        )
        
        if file_path:
            self.load_image(file_path)
    
    def drop_image(self, event):
        """
        (Gestione dell'immagine - punto 2)
        Gestisce il drop di un'immagine.
        """
        if not USE_DND:
            return
            
        try:
            file_path = event.data
            
            # Rimuove le parentesi graffe se presenti (tipico di Windows)
            if file_path.startswith("{") and file_path.endswith("}"):
                file_path = file_path[1:-1]
                
            # Verifica che sia un file immagine
            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                self.load_image(file_path)
            else:
                messagebox.showwarning("Formato non supportato", "Seleziona un'immagine in formato PNG, JPG o JPEG.")
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare l'immagine: {str(e)}")
    
    def load_image(self, file_path):
        """
        (Gestione dell'immagine - punto 2)
        Carica un'immagine dal percorso specificato.
        """
        try:
            # Salva il percorso dell'immagine
            self.image_path = file_path
            self.path_label.config(text=f"Selezionato: {os.path.basename(file_path)}")
            
            # Carica l'immagine e crea una miniatura
            img = Image.open(file_path)
            img.thumbnail((200, 200))
            self.thumbnail = ImageTk.PhotoImage(img)
            
            # Aggiorna l'etichetta della miniatura
            self.thumbnail_label.config(image=self.thumbnail, text="")
            
            # Codifica l'immagine in base64 per l'invio all'API
            with open(file_path, "rb") as img_file:
                self.image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            self.image_loaded = True
            self.add_message("Sistema", f"Immagine caricata: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare l'immagine: {str(e)}")
    
    def add_message(self, sender, message):
        """
        Aggiunge un messaggio alla chat.
        """
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
    
    def interactive_chat(self):
        """
        (Interazione con il modello di IA - punto 3)
        Gestisce l'interazione con il modello di IA.
        """
        user_text = self.user_input.get().strip()
        
        # Verifica che ci sia del testo
        if not user_text:
            messagebox.showinfo("Input mancante", "Inserisci un messaggio.")
            return
        
        # Aggiunge il messaggio dell'utente alla chat
        self.add_message("Tu", user_text)
        
        # Pulisce il campo di input
        self.user_input.delete(0, tk.END)
        
        # Ottiene la risposta dal modello
        try:
            response = self._chat_gpt_fn(self, user_text, self.image_base64 if self.image_loaded else "")
            self.add_message("AI", response)
        except Exception as e:
            error_msg = f"Errore nella chiamata al modello: {str(e)}"
            self.add_message("Sistema", error_msg)
            messagebox.showerror("Errore", error_msg)
    
    def dummy_chat_bot(self, user_text, image_base64):
        """
        Funzione di esempio per il chatbot.
        Restituisce una risposta predefinita.
        """
        if image_base64:
            return f"Ho ricevuto la tua immagine e il tuo messaggio: '{user_text}'. Questa è una risposta di esempio."
        else:
            return f"Ho ricevuto il tuo messaggio: '{user_text}'. Carica un'immagine per l'analisi."
    
    def on_enter_pressed(self, event):
        self.interactive_chat()
        return "break"

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Create the main window
    if USE_DND:
        try:
            root = TkinterDnD.Tk()
            print("Using TkinterDnD.Tk()")
        except Exception as e:
            print(f"Error creating TkinterDnD.Tk(): {e}")
            root = tk.Tk()
            print("Falling back to tk.Tk()")
    else:
        root = tk.Tk()
        print("Using tk.Tk()")
    
    # Check if we should use the real model or dummy model
    use_real_model = os.environ.get("USE_REAL_MODEL", "0") == "1"
    
    if use_real_model:
        try:
            # Import the real_model from the same directory
            from real_model_integration import real_model
            app = ImageAnalysisChatBot(root, chat_gpt_fn=real_model)
            print("Using real OpenAI model for chat")
        except ImportError as e:
            print(f"Error importing real model: {e}")
            app = ImageAnalysisChatBot(root)
            print("Using dummy model for chat")
    else:
        app = ImageAnalysisChatBot(root)
        print("Using dummy model for chat")
    
    root.mainloop() 