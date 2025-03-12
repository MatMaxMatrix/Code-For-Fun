# PDF Creator from CSV

This program generates personalized PDF files for each person listed in a CSV file. Each PDF includes the person's name, company, and a grid of discount images.

## Requirements

- Python 3.6 or higher
- ReportLab library (`pip install reportlab`)

## Setup

1. Make sure you have the required Python packages installed:
   ```
   pip install reportlab
   ```

2. Prepare your discount images:
   - Create a folder named `images` in the same directory as the script
   - Add your discount images with filenames: `sconto1.jpg`, `sconto2.jpg`, ..., `sconto8.jpg`
   - Images should be in JPG format

3. Prepare your CSV file:
   - Create a file named `partecipanti.csv` in the same directory as the script
   - The CSV should have at least two columns: name and company
   - The first row should be the header row
   - Example:
     ```
     Nome,Azienda
     Mario Rossi,ABC Company
     Anna Bianchi,XYZ Corporation
     ```

## Usage

Run the script:
```
python org.py
```

or

```
python pdf_creator.py
```

The program will:
1. Check if the `images` directory exists, and create it if it doesn't
2. Check if the CSV file exists, and create a sample if it doesn't
3. Generate a PDF for each person in the CSV file
4. Save the PDFs in an `output` directory

## Output

- All generated PDFs will be saved in the `output` directory
- Each PDF will be named after the person (spaces replaced with underscores)
- Example: `Mario_Rossi.pdf`

## Customization

You can modify the script to:
- Change the page layout
- Adjust text positioning and font sizes
- Change the number and layout of discount images
- Add additional content to the PDFs 