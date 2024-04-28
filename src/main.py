from pathlib import Path
from config import COMPANY_NUMBERS, TESSERACT_PATH, SEARCH_TERMS
from api_client import APIClient
from rate_limiter import RateLimiter
from file_manager import FileManager
from src.ocr import OCR
from src.pdf_search import search_pdf_and_output_to_csv
import logging


def download_financials(company_number, limiter):
    # Check if the company folder already exists if the downloaded_pdfs directory already exists
    if Path("./data/downloaded_pdfs").exists():
        base_dir = Path("./data/downloaded_pdfs")
        company_folder = None
        for folder in base_dir.iterdir():
            if folder.is_dir() and folder.name.startswith(company_number):
                company_folder = folder
                break
        if company_folder is not None and company_folder.exists():
            print(f"Company folder already exists for {company_number}. Skipping")
            return

    client = APIClient(limiter)
    response = client.get_company_profile(company_number)
    if response.status_code == 200:
        company_profile = response.json()
        print(
            f"Processing company: {company_profile['company_name']} ({company_number})"
        )
        manager = FileManager(
            f"./data/downloaded_pdfs/{company_number}-{company_profile['company_name']}",
            limiter,
        )
        start_index = 0
        more_pages = True
        while more_pages:
            history_response = client.get_filing_history_page(
                company_number, start_index
            )
            if history_response.status_code == 200:
                filing_history = history_response.json()
                for item in filing_history["items"]:
                    if "accounts" in item["description"].lower():
                        print(f"Accounts related document found: {item['description']}")
                        doc_metadata_response = client.get_document_metadata(
                            item["links"]["document_metadata"]
                        )
                        if doc_metadata_response.status_code == 200:
                            doc_metadata = doc_metadata_response.json()
                            download_url = doc_metadata["links"]["document"]
                            filename = f"{item['date']}_{item['description'].replace(' ', '_')}.pdf"
                            manager.download_pdf(download_url, filename)
                        else:
                            print("Failed to retrieve document metadata")

                start_index += len(filing_history["items"])
                more_pages = start_index < filing_history["total_count"]
            else:
                raise Exception("Failed to retrieve filing history")
    else:
        raise Exception("Failed to retrieve company profile")


def ocr_financials(company_number):
    ocr_processor = OCR(TESSERACT_PATH)

    # The base directory where company folders are located
    base_dir = Path("./data/downloaded_pdfs")

    # Find the directory that starts with the company number
    for folder in base_dir.iterdir():
        if folder.is_dir() and folder.name.startswith(company_number):
            folder_path = str(folder)
            files = ocr_processor.list_files_in_directory(folder_path)
            output_dir = Path(f"./data/searchable_pdfs/{folder.name}")
            output_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                pdf_path = folder_path + "/" + file
                output_path = str(output_dir / f"searchable_{file}")
                ocr_processor.perform_ocr_on_pdf(pdf_path, output_path)
            break
    else:
        print(f"No directory found for company number {company_number}")


def analyze_company(company_number):
    base_dir = Path("./data/searchable_pdfs")
    # Find the directory that starts with the company number
    company_folder = None
    for folder in base_dir.iterdir():
        if folder.is_dir() and folder.name.startswith(company_number):
            company_folder = folder
            break
    if company_folder is None:
        print(f"No directory found for company number {company_number}")
        return
    pdf_dir_path = str(company_folder)
    output_csv_path = "./data/term_counts.csv"
    search_pdf_and_output_to_csv(pdf_dir_path, SEARCH_TERMS, output_csv_path)


if __name__ == "__main__":
    limiter = RateLimiter(590, 300)
    for i in range(3):
        for number in COMPANY_NUMBERS:
            try:
                if i == 0:
                    logging.info(f"Downloading financials for company {number}")
                    download_financials(number, limiter)
                elif i == 1:
                    logging.info(f"Performing OCR on financials for company {number}")
                    ocr_financials(number)
                else:
                    logging.info(f"Analyze company {number}")
                    analyze_company(number)
                    pass
            except Exception as e:
                print(f"Error processing company {number}: {e}")
