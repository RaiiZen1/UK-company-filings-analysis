import pandas as pd

API_KEY = "3ef1fc14-2fef-4400-ae57-bfb43b8103d0"
BASE_URL = "https://api.companieshouse.gov.uk"
TESSERACT_PATH = r"S:\Users\Hiwi\Plastic Tax\Program Files\Tesseract\tesseract.exe"
try:
    COMPANY_NUMBERS = pd.read_csv("./data/company_ids.csv")["company_ids"].tolist()
except FileNotFoundError:
    COMPANY_NUMBERS = []
# COMPANY_NUMBERS = ["01087941", "04168334", "02019274"] # For testing
SEARCH_TERMS = ["plastic", "plastic tax", "plastic levy", "environmental tax"]
# SEARCH_TERMS = ["company", "accounts", "financial", "tax"] # For testing
DOWNLOAD_FINANCIALS = False
OCR_PDFS = True
ANALYZE_PDFS = True
