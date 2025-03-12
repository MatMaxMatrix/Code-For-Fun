import os
import sys
from pathlib import Path
import PyPDF2
from PyPDF2 import PdfReader

def check_pdf_for_images(pdf_path):
    """Check if a PDF contains images and print information about them."""
    print(f"Checking PDF: {pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
        page = reader.pages[0]  # Get the first page
        
        # Check if the page has XObjects (which include images)
        if '/XObject' in page['/Resources']:
            xobjects = page['/Resources']['/XObject']
            
            if xobjects:
                print(f"Found {len(xobjects)} XObjects (potential images)")
                for key, obj in xobjects.items():
                    if obj['/Subtype'] == '/Image':
                        print(f"  - Image found: {key}")
                        print(f"    Width: {obj['/Width']}, Height: {obj['/Height']}")
                        print(f"    Filter: {obj.get('/Filter', 'None')}")
                        print(f"    ColorSpace: {obj.get('/ColorSpace', 'None')}")
                return True
            else:
                print("No XObjects found in the PDF")
                return False
        else:
            print("No XObjects resource found in the PDF")
            return False
    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        return False

def main():
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Find all PDF files in the current directory
    pdf_files = list(current_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in the current directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF files.")
    
    # Check the first PDF file
    sample_pdf = pdf_files[0]
    has_images = check_pdf_for_images(sample_pdf)
    
    if has_images:
        print(f"\nThe PDF {sample_pdf.name} contains images.")
    else:
        print(f"\nThe PDF {sample_pdf.name} does not contain images.")
        print("You may need to adjust your PDF generation code to properly include images.")

if __name__ == "__main__":
    main() 