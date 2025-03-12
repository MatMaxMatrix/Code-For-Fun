import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import os

# Funzione per creare il PDF
def create_pdf(name, company, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    # Assicuriamo che il testo sia visibile impostando il colore
    c.setFillColor(colors.black)
    
    # Calcolo della larghezza del testo per un centramento più preciso
    def center_text(text, font_name, font_size, y_position):
        c.setFont(font_name, font_size)
        text_width = pdfmetrics.stringWidth(text, font_name, font_size)
        c.drawString((width - text_width) / 2, y_position, text)
    
    # Posizionamento del testo
    center_text(name, "Helvetica-Bold", 24, height - 100)
    center_text(company, "Helvetica", 18, height - 130)
    center_text("Ecco gli sconti a te riservati", "Helvetica", 14, height - 160)
    
    # Aggiunta delle 8 immagini
    image_width = width / 4
    image_height = height / 6
    
    for i in range(8):
        image_path = f"sconto{i+1}.jpg"  # Assumendo le immagini siano nella stessa cartella
        
        # Verifica se l'immagine esiste
        if os.path.exists(image_path):
            try:
                x = (i % 4) * image_width
                y = height - 200 - ((i // 4) * image_height) - image_height  # Correggiamo la posizione Y
                c.drawImage(image_path, x, y, width=image_width, height=image_height)
            except Exception as e:
                print(f"Errore nel caricare l'immagine {image_path}: {e}")
        else:
            print(f"Attenzione: Immagine {image_path} non trovata")
    
    # Salva il PDF
    c.showPage()  # Assicura che tutte le operazioni siano concluse
    c.save()
    print(f"PDF creato: {pdf_filename}")

# Lettura del CSV e creazione dei PDF
def create_pdfs_from_csv(csv_file):
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Salta la prima riga (intestazione)
            print(f"Intestazioni CSV: {header}")
            
            count = 0
            for row in reader:
                if len(row) >= 2:  # Verifica che ci siano almeno due colonne
                    name, company = row[0], row[1]
                    # Crea un nome file valido sostituendo i caratteri non validi
                    safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in name)
                    pdf_filename = f"{safe_name.replace(' ', '_')}.pdf"
                    create_pdf(name, company, pdf_filename)
                    count += 1
                else:
                    print(f"Riga saltata (formato non valido): {row}")
            
            print(f"Totale PDF creati: {count}")
    except Exception as e:
        print(f"Errore nella lettura del file CSV: {e}")

# Esegui la funzione di generazione dei PDF
if __name__ == "__main__":
    csv_file = 'partecipanti.csv'
    if os.path.exists(csv_file):
        create_pdfs_from_csv(csv_file)
    else:
        print(f"File CSV non trovato: {csv_file}")