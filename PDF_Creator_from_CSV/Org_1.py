import csv
import os
import subprocess
import shutil
import tempfile
import base64

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Template HTML per ogni PDF - using absolute paths for images
html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sconti per {name}</title>
    <style>
        @page {{ size: A4; margin: 0; }}
        body {{ text-align: center; font-family: Helvetica, Arial; padding: 20px; margin: 0; height: 100vh; 
               display: flex; flex-direction: column; }}
        .header {{ margin-bottom: 20px; }}
        .name {{ font-size: 24px; font-weight: bold; margin-bottom: 10px; }}
        .company {{ font-size: 18px; margin-bottom: 10px; }}
        .message {{ font-size: 14px; margin-bottom: 20px; }}
        .images {{ display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(2, 1fr);
                  gap: 15px; width: 100%; flex-grow: 1; }}
        .images img {{ width: 100%; height: 100%; object-fit: contain; border: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="name">{name}</div>
        <div class="company">{company}</div>
        <div class="message">Ecco gli sconti a te riservati</div>
    </div>
    <div class="images">
        {image_tags}
    </div>
</body>
</html>'''

# Embed image as base64 or reference based on availability
def get_image_tags():
    image_tags = []
    for i in range(1, 9):
        img_path = os.path.join(current_dir, f"sconto{i}.jpg")
        if os.path.exists(img_path):
            # Use data URI to embed images directly in HTML
            with open(img_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                image_tags.append(f'<img src="data:image/jpeg;base64,{img_data}">')
        else:
            # If image doesn't exist, use a placeholder
            image_tags.append(f'<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAABmJLR0QA/wD/AP+gvaeTAAAA20lEQVR4nO3bMQ0AIAwAwQpAYgErWMEKVrAgNiDhHbj/NNlk2wYAAAAAAAAAAAAAADCqbJKyt+fHvT0+NhRCIFMCmRLIlECmBDIlkCmBTAlkSiBTApkSyJRApgQyJZApgUwJZEogUwKZEsiUQKYEMiWQKYFMCWRKIFMCmRLIlECmBDIlkCmBTAlkSiBTApkSyJRApgQyJZApgUwJZEogUwKZEsiUQKYEMiWQKYFMCWRKIFMCmRLIlECmBDIlkCmBTAlkSiBTApkSyJRApgQyJZApgUwJZEogUwIBAAAAAAAAAAAAwHceLPA9cLyFVlQAAAAASUVORK5CYII=" alt="Missing Image">')
    return '\n'.join(image_tags)

# Create PDF with wkhtmltopdf
def create_pdf_wkhtmltopdf(csv_file):
    # Generate the image tags with embedded base64 data
    image_tags = get_image_tags()
    
    # Process CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        
        for row in reader:
            try:
                name, company = row
                
                # Create a temporary directory for this PDF
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Create temporary HTML file
                    temp_html = os.path.join(temp_dir, f"temp_{name.replace(' ', '_')}.html")
                    
                    # Generate HTML content with embedded images
                    html_content = html_template.format(
                        name=name,
                        company=company,
                        image_tags=image_tags
                    )
                    
                    with open(temp_html, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    # Generate PDF
                    pdf_name = os.path.join(current_dir, f"{name.replace(' ', '_')}.pdf")
                    
                    # Run wkhtmltopdf command
                    cmd = [
                        'wkhtmltopdf',
                        '--enable-local-file-access',
                        '--page-size', 'A4',
                        '--orientation', 'Portrait',
                        '--disable-smart-shrinking',
                        '--no-background',
                        '--margin-top', '0', '--margin-bottom', '0', '--margin-left', '0', '--margin-right', '0',
                        '--zoom', '1.0',
                        '--javascript-delay', '1000',
                        temp_html,
                        pdf_name
                    ]
                    
                    # Execute command
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    # Check result
                    if result.returncode != 0:
                        print(f"Error creating PDF for {name}: {result.stderr}")
                    else:
                        print(f"Successfully created PDF for {name}")
            
            except ValueError:
                print(f"Skipping malformed row: {row}")
            except Exception as e:
                print(f"Error processing {row}: {str(e)}")

if __name__ == "__main__":
    create_pdf_wkhtmltopdf(os.path.join(current_dir, 'partecipanti.csv'))