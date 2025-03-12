import os
import subprocess

def check_pdf_for_images(pdf_file):
    """Check if a PDF file contains image references using pdfinfo"""
    try:
        # Run pdfinfo to get basic info about the PDF
        result = subprocess.run(['pdfinfo', pdf_file], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        
        if result.returncode != 0:
            print(f"Error running pdfinfo on {pdf_file}: {result.stderr}")
            return False
        
        # Print the PDF info
        print(f"PDF Info for {pdf_file}:")
        print(result.stdout)
        
        # Check file size as a basic indicator
        file_size = os.path.getsize(pdf_file)
        print(f"File size: {file_size} bytes")
        
        # If file size is very small, it might not contain images
        if file_size < 5000:
            print("Warning: PDF file is very small, might not contain images")
        
        return True
    except Exception as e:
        print(f"Error checking PDF {pdf_file}: {e}")
        return False

def main():
    output_dir = 'pdf_output'
    
    # Check if output directory exists
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist")
        return
    
    # Get all PDF files in the output directory
    pdf_files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {output_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    
    # Check the first PDF file
    first_pdf = os.path.join(output_dir, pdf_files[0])
    check_pdf_for_images(first_pdf)

if __name__ == "__main__":
    main() 