from config import COMPANY_NUMBERS, TESSERACT_PATH, SEARCH_TERMS
from api_client import APIClient
from rate_limiter import RateLimiter
from file_manager import FileManager
from src.ocr import OCR
from src.pdf_search import search_pdf_and_output_to_csv
import logging


def download_financials(company_number):
    client = APIClient()
    limiter = RateLimiter(600, 300)
    manager = FileManager(f"./data/downloaded_pdfs/{company_number}")

    response = client.get_company_profile(company_number)
    if response.status_code == 200:
        company_profile = response.json()
        print(
            f"Processing company: {company_profile['company_name']} ({company_number})"
        )

        start_index = 0
        more_pages = True
        while more_pages:
            limiter.check()
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
    folder_path = f"./data/downloaded_pdfs/{company_number}/"
    files = ocr_processor.list_files_in_directory(folder_path)
    for file in files:
        pdf_path = f"{folder_path}{file}"
        output_path = f"./data/searchable_pdfs/{company_number}/searchable_{file}"
        ocr_processor.perform_ocr_on_pdf(pdf_path, output_path)


def analyze_company(company_number):
    pdf_dir_path = f"./data/searchable_pdfs/{company_number}"
    output_csv_path = "./data/term_counts.csv"
    search_pdf_and_output_to_csv(pdf_dir_path, SEARCH_TERMS, output_csv_path)


if __name__ == "__main__":
    for i in range(3):
        for number in COMPANY_NUMBERS:
            try:
                if i == 0:
                    logging.info(f"Downloading financials for company {number}")
                    download_financials(number)
                elif i == 1:
                    logging.info(f"Performing OCR on financials for company {number}")
                    ocr_financials(number)
                else:
                    logging.info(f"Analyze company {number}")
                    analyze_company(number)
                    pass
            except Exception as e:
                print(f"Error processing company {number}: {e}")
