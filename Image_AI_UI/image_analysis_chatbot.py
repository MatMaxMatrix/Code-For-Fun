# image_analysis_chatbot.py
import tkinter as tk
from tkinter import filedialog, messagebox
import base64
from PIL import Image, ImageTk
import os

# Verifica il supporto per drag & drop
USE_DND = False
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    test_root = tk.Tk()
    try:
        test_root.tk.call('package', 'require', 'tkdnd')
        USE_DND = True
    except tk.TclError:
        print("pacchetto tkdnd non disponibile")
    finally:
        test_root.destroy()
except ImportError:
    print("modulo tkinterdnd2 non disponibile")

class Response:
    """Contenitore semplice per le risposte"""
    def __init__(self, message):
        self.message = message

class ImageAnalysisChatBot:
    """ChatBot per l'analisi delle immagini con interfaccia grafica"""
    
    def __init__(self, tk_root, chat_gpt_fn=None):
        self.root = tk_root
        self.root.title("ChatBot: Analisi Immagini")
        self.root.geometry("800x600")
        
        # Variabili per l'immagine
        self.image_path = ""
        self.image_base64 = ""
        self.image_loaded = False
        self.thumbnail = None
        
        # Usa la funzione dummy se non ne viene fornita una
        self._chat_gpt_fn = chat_gpt_fn or self.dummy_chat_bot
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame superiore: Selezione immagine e miniatura
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.btn_select_image = tk.Button(top_frame, text="Seleziona immagine", command=self.select_image)
        self.btn_select_image.pack(side=tk.LEFT)
        
        self.thumbnail_label = tk.Label(top_frame, text="Nessuna immagine\ncaricata", 
                                       width=120, height=100, bg="lightgrey", relief="sunken")
        self.thumbnail_label.pack(side=tk.LEFT, padx=10)
        
        # Abilita drag & drop se disponibile
        if USE_DND:
            try:
                self.thumbnail_label.drop_target_register(DND_FILES)
                self.thumbnail_label.dnd_bind('<<Drop>>', self.drop_image)
            except Exception as e:
                print(f"Errore nell'impostazione del drag & drop: {e}")
        
        # Area chat con barra di scorrimento
        self.chat_canvas = tk.Canvas(self.root, borderwidth=0, background="#f0f0f0")
        self.chat_frame = tk.Frame(self.chat_canvas, background="#f0f0f0")
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.chat_canvas.yview)
        self.chat_canvas.configure(yscrollcommand=self.vsb.set)
        
        self.vsb.pack(side="right", fill="y")
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_canvas.create_window((4,4), window=self.chat_frame, anchor="nw", tags="chat_frame")
        self.chat_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        
        # Frame inferiore: Input e pulsante di invio
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        self.input_box = tk.Entry(bottom_frame)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
        self.input_box.bind("<Return>", lambda e: self.interactive_chat())
        
        self.send_button = tk.Button(bottom_frame, text="Invia", command=self.interactive_chat)
        self.send_button.pack(side=tk.RIGHT)
        
    def append_message(self, author, message):
        """Aggiunge un messaggio alla chat con formattazione a bolla"""
        msg_frame = tk.Frame(self.chat_frame, bg="#f0f0f0", pady=5)
        msg_frame.pack(fill=tk.X, anchor="w" if author=="user" else "e", padx=10)
        
        bubble_bg = "#cce5ff" if author=="user" else "#d4edda"
        label = tk.Label(msg_frame, text=message, bg=bubble_bg, wraplength=500, 
                        justify="left", padx=10, pady=5)
        label.pack(side="left")
        
    def select_image(self):
        """Permette all'utente di selezionare un file immagine"""
        file_path = filedialog.askopenfilename(
            title="Seleziona un'immagine",
            filetypes=[("File Immagine", "*.png *.jpg *.jpeg"), ("Tutti i File", "*.*")]
        )
        if file_path:
            self.load_image(file_path)
            
    def drop_image(self, event):
        """Gestisce il caricamento dell'immagine tramite drag & drop"""
        files = self.root.tk.splitlist(event.data)
        if files:
            self.load_image(files[0])
            
    def load_image(self, file_path):
        """Carica l'immagine, la codifica in base64, crea una miniatura"""
        try:
            self.image_path = file_path
            # Legge e codifica l'immagine
            with open(file_path, "rb") as f:
                self.image_base64 = base64.b64encode(f.read()).decode('utf-8')
            self.image_loaded = True
            
            # Crea miniatura
            image = Image.open(file_path)
            image.thumbnail((100, 100))
            self.thumbnail = ImageTk.PhotoImage(image)
            self.thumbnail_label.configure(image=self.thumbnail, text="")
            
            self.append_message("system", "Immagine caricata con successo!")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel caricamento dell'immagine:\n{e}")
            
    def dummy_chat_bot(self, user_text, image_base64):
        """Simula la risposta del modello AI"""
        return Response(f"Risposta dummy. Prompt: {user_text}\nRisposta: Risposta di test.")

    def chat_fn(self, user_text):
        """Chiama la funzione chatbot con gestione degli errori"""
        try:
            return self._chat_gpt_fn(user_text, self.image_base64 if self.image_loaded else None)
        except Exception as e:
            messagebox.showerror("Errore API", f"Errore durante la chiamata alle API:\n{e}")
            return None

    def interactive_chat(self):
        """Gestisce l'invio dei messaggi, la chiamata API e la visualizzazione delle risposte"""
        user_text = self.input_box.get().strip()
        if not user_text:
            messagebox.showwarning("Input mancante", "Inserisci un messaggio.")
            return
        
        self.append_message("user", user_text)
        self.input_box.delete(0, tk.END)
        
        response = self.chat_fn(user_text)
        if response:
            self.append_message("bot", response.message.strip())
        else:
            self.append_message("bot", "Errore nella chiamata API.")

# Esecuzione principale
if __name__ == "__main__":
    # Inizializza la finestra root con supporto drag & drop se disponibile
    root = TkinterDnD.Tk() if USE_DND else tk.Tk()
    
    # Controlla se utilizzare il modello reale o dummy
    use_real_model = os.environ.get("USE_REAL_MODEL", "0") == "1"
    
    if use_real_model:
        try:
            from real_model_integration import real_model
            app = ImageAnalysisChatBot(root, chat_gpt_fn=real_model)
            print("Utilizzo del modello OpenAI reale")
        except ImportError as e:
            app = ImageAnalysisChatBot(root)
            print(f"Errore nell'importazione del modello reale: {e}. Utilizzo del modello dummy")
    else:
        app = ImageAnalysisChatBot(root)
        print("Utilizzo del modello dummy")
    
    root.mainloop()