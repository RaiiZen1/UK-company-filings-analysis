# UK-company-filings-analysis
A Python tool for automating the extraction and analysis of UK corporate filings to identify references to 'plastic tax' and related environmental terms. This project involves downloading PDFs, converting them to searchable text via OCR, and performing keyword searches

# Installation
- Setup virtual environment
- Install Tesseract
- Locate the tesseract.exe file and set the location in the .env file

# Convert PDF Table to CSV
- First crop the PDF to only include actual table data
- Go to https://www.ilovepdf.com/de/pdf_zu_excel
- Upload the PDF and convert
- Open the converted Excel 
- Copy the column containing the company numbers
- Paste them into a new .csv file 
- Store the file in ./data/company_ids.cdv
