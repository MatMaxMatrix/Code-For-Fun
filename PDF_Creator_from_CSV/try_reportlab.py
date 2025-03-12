import csv
import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm

# Get the absolute path to the current directory
current_dir = Path(__file__).parent

def create_pdf_reportlab(csv_file):
    """Create PDFs using reportlab with images in a grid layout."""
    # Load image paths
    image_paths = []
    for i in range(1, 9):
        img_path = current_dir / f"sconto{i}.jpg"
        if img_path.exists():
            image_paths.append(str(img_path))
        else:
            print(f"Warning: Image {img_path} not found")
    
    if not image_paths:
        print("No images found. Please check the image files.")
        return
    
    # Process CSV file
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            try:
                name, company = row
                create_single_pdf(name, company, image_paths)
            except ValueError:
                print(f"Skipping malformed row: {row}")
            except Exception as e:
                print(f"Error processing {row}: {str(e)}")

def create_single_pdf(name, company, image_paths):
    """Create a single PDF for a person with images in a grid."""
    pdf_name = current_dir / f"{name.replace(' ', '_')}.pdf"
    doc = SimpleDocTemplate(str(pdf_name), pagesize=A4, 
                           rightMargin=0.5*cm, leftMargin=0.5*cm,
                           topMargin=0.5*cm, bottomMargin=0.5*cm)
    
    # Create styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=24,
        alignment=1,  # Center alignment
        spaceAfter=10
    )
    company_style = ParagraphStyle(
        'Company',
        parent=styles['Normal'],
        fontSize=18,
        alignment=1,
        spaceAfter=5
    )
    message_style = ParagraphStyle(
        'Message',
        parent=styles['Normal'],
        fontSize=14,
        alignment=1,
        spaceAfter=15
    )
    
    # Create content
    elements = []
    
    # Add header
    elements.append(Paragraph(name, title_style))
    elements.append(Paragraph(company, company_style))
    elements.append(Paragraph("Ecco gli sconti a te riservati", message_style))
    
    # Create a 4x2 grid of images
    # First, prepare the images with consistent size
    image_objects = []
    for img_path in image_paths:
        img = Image(img_path)
        # Set a consistent width while maintaining aspect ratio
        img.drawWidth = 3.5 * cm
        img.drawHeight = 3.5 * cm
        image_objects.append(img)
    
    # Create two rows of 4 images each
    row1 = image_objects[:4]
    row2 = image_objects[4:8] if len(image_objects) > 4 else []
    
    # Create a table for the grid layout
    data = [row1]
    if row2:
        data.append(row2)
    
    # Create the table with the images
    table = Table(data, colWidths=[4*cm]*4, rowHeights=[4*cm]*len(data))
    
    # Add style to the table
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    
    # Build the PDF
    try:
        doc.build(elements)
        print(f"Successfully created PDF for {name}")
    except Exception as e:
        print(f"Error creating PDF for {name}: {str(e)}")

if __name__ == "__main__":
    create_pdf_reportlab(current_dir / 'partecipanti.csv') 