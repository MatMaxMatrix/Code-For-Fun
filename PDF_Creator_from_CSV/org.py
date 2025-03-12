import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Funzione per creare il PDF
def create_pdf(name, company, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    # Posizionamento del testo
    c.setFont("Helvetica-Bold", 24)
    c.drawString(width / 2 - len(name) * 6, height - 100, name)  # Nome centrato
    
    c.setFont("Helvetica", 18)
    c.drawString(width / 2 - len(company) * 6, height - 130, company)  # Azienda centrato
    
    c.setFont("Helvetica", 14)
    c.drawString(width / 2 - len("Ecco gli sconti a te riservati") * 3, height - 160, "Ecco gli sconti a te riservati")
    
    # Aggiunta delle 8 immagini
    image_width = width / 4  # Impostiamo una dimensione rettangolare
    image_height = height / 6
    
    for i in range(8):
        image_path = f"sconto{i+1}.jpg"  # Assumendo le immagini siano nella stessa cartella
        x = (i % 4) * image_width
        y = height - 200 - (i // 4) * image_height
        c.drawImage(image_path, x, y, width=image_width, height=image_height)
    
    c.save()

# Lettura del CSV e creazione dei PDF
def create_pdfs_from_csv(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Salta la prima riga (intestazione)
        
        for row in reader:
            name, company = row
            pdf_filename = f"{name.replace(' ', '_')}.pdf"
            create_pdf(name, company, pdf_filename)

# Esegui la funzione di generazione dei PDF
csv_file = 'partecipanti.csv'  # Assicurati che il CSV sia nel formato giusto
create_pdfs_from_csv(csv_file)