import os
import subprocess
import tempfile
import shutil

# Create a very simple HTML with just one image
html_content = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Image</title>
    <style>
        body { text-align: center; }
        img { width: 300px; height: auto; border: 1px solid red; }
    </style>
</head>
<body>
    <h1>Test Image</h1>
    <img src="sconto1.jpg">
</body>
</html>
'''

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create a temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    print(f"Created temporary directory: {temp_dir}")
    
    # Copy the first image to the temp directory
    src_img = os.path.join(current_dir, "sconto1.jpg")
    dst_img = os.path.join(temp_dir, "sconto1.jpg")
    
    if os.path.exists(src_img):
        shutil.copy2(src_img, dst_img)
        print(f"Copied image to {dst_img}")
        
        # Check image file size
        img_size = os.path.getsize(dst_img)
        print(f"Image size: {img_size} bytes")
        
        # Create HTML file in the temp directory
        html_file = os.path.join(temp_dir, "test.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Change to the temp directory
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        
        # Create PDF
        pdf_file = os.path.join(current_dir, "test_image.pdf")
        cmd = [
            'wkhtmltopdf',
            '--enable-local-file-access',
            '--debug-javascript',
            'test.html',
            pdf_file
        ]
        
        print(f"Running command from {os.getcwd()}: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Change back to original directory
        os.chdir(original_dir)
        
        if result.returncode != 0:
            print(f"Error creating PDF: {result.stderr}")
        else:
            print(f"Successfully created test PDF at {pdf_file}")
            print(f"PDF size: {os.path.getsize(pdf_file)} bytes")
    else:
        print(f"ERROR: Image not found at {src_img}") 