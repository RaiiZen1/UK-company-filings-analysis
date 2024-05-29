import pandas as pd

API_KEY = "3ef1fc14-2fef-4400-ae57-bfb43b8103d0"
BASE_URL = "https://api.companieshouse.gov.uk"
TESSERACT_PATH = r"S:\Users\Hiwi\Plastic Tax\Program Files\Tesseract\tesseract.exe"

SEARCH_TERMS = [
    "plastic",
    "plastic tax",
    "plastic levy",
    "environmental tax",
]  # Edit this
DOWNLOAD_FINANCIALS = False  # Edit this
OCR_PDFS = False  # Edit this
ANALYZE_PDFS = True  # Edit this

try:
    COMPANY_NUMBERS = pd.read_csv("./data/company_ids.csv")["company_ids"].tolist()
except FileNotFoundError:
    COMPANY_NUMBERS = []
