import csv
import os
import subprocess
import base64
from pathlib import Path

# Ottieni il percorso assoluto della directory corrente
current_dir = Path(__file__).parent

def image_to_base64(image_path):
    """Converti un'immagine in codifica base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Template HTML con CSS
html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sconti per {name}</title>
    <style>
        @page {{ size: A4; margin: 0; }}
        body {{ 
            text-align: center; 
            font-family: Helvetica, Arial, sans-serif; 
            padding: 10px; 
            margin: 0; 
            height: 100vh; 
            display: flex; 
            flex-direction: column; 
        }}
        .header {{ margin-bottom: 10px; }}
        .name {{ font-size: 24px; font-weight: bold; margin-bottom: 5px; }}
        .company {{ font-size: 18px; margin-bottom: 5px; }}
        .message {{ font-size: 14px; margin-bottom: 10px; }}
        .images {{ 
            display: grid; 
            grid-template-columns: repeat(2, 1fr); 
            grid-template-rows: repeat(4, 1fr);
            gap: 10px; 
            width: 100%; 
            flex-grow: 1; 
        }}
        .image-container {{ 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            border: 1px solid #ddd; 
            padding: 5px; 
            height: 120px; 
            box-sizing: border-box; 
            background-color: #ffffff;
        }}
        img {{ 
            display: block; 
            max-width: 100%; 
            max-height: 100%; 
            object-fit: contain; 
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="name">{name}</div>
        <div class="company">{company}</div>
        <div class="message">Ecco gli sconti a te riservati</div>
    </div>
    <div class="images">
        {images}
    </div>
</body>
</html>'''

def create_pdf(csv_file):
    """Crea PDF utilizzando wkhtmltopdf con immagini in una griglia."""
    # Genera i tag delle immagini
    image_tags = []
    for i in range(1, 9):
        img_path = current_dir / f"sconto{i}.jpg"
        if img_path.exists():
            base64_data = image_to_base64(img_path)
            img_tag = f'<img src="data:image/jpeg;base64,{base64_data}" alt="Sconto {i}" style="max-width:100%; max-height:100%;">'
        else:
            # Usa un segnaposto vuoto se l'immagine non esiste
            img_tag = '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="Missing Image">'
        image_tags.append(f'<div class="image-container">{img_tag}</div>')
    
    image_html = '\n'.join(image_tags)
    
    # Elabora il CSV e crea i PDF
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Salta l'intestazione
        for row in reader:
            try:
                name, company = row
                # Genera il contenuto HTML
                html_content = html_template.format(
                    name=name,
                    company=company,
                    images=image_html
                )
                
                # Salva HTML in un file temporaneo
                html_file = current_dir / f"temp_{name.replace(' ', '_')}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Genera il PDF
                pdf_file = current_dir / f"{name.replace(' ', '_')}.pdf"
                cmd = [
                    "wkhtmltopdf",
                    "--enable-local-file-access",
                    "--page-size", "A4",
                    "--margin-top", "5mm",
                    "--margin-right", "5mm",
                    "--margin-bottom", "5mm",
                    "--margin-left", "5mm",
                    "--no-stop-slow-scripts",
                    "--disable-smart-shrinking",
                    str(html_file),
                    str(pdf_file)
                ]
                
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Rimuovi il file HTML temporaneo
                os.remove(html_file)
                
            except Exception as e:
                print(f"Errore nell'elaborazione di {name if 'name' in locals() else row}: {str(e)}")

if __name__ == "__main__":
    create_pdf(current_dir / 'partecipanti.csv')