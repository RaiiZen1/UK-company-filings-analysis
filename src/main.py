from pathlib import Path
from config import (
    COMPANY_NUMBERS,
    TESSERACT_PATH,
    SEARCH_TERMS,
    DOWNLOAD_FINANCIALS,
    OCR_PDFS,
    ANALYZE_PDFS,
)
from api_client import APIClient
from rate_limiter import RateLimiter
from file_manager import FileManager
from src.ocr import OCR
from src.pdf_search import search_pdf_and_output_to_csv
import logging
import concurrent.futures

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def download_financials(company_number, limiter):
    """
    Download financial documents for a given company.

    Checks if the company's folder already exists to avoid redundancy. If not, it retrieves the company's
    profile and iterates over its filing history to download PDFs related to financial accounts.

    Args:
    company_number (str): The company number for which to download financials.
    limiter (RateLimiter): A rate limiter object to manage API call rates.

    Raises:
    Exception: If there is an error in fetching company profile or filing history.
    """
    base_dir = Path("./data/downloaded_pdfs")
    # Ensure base directory for downloaded PDFs exists
    if base_dir.exists():
        for folder in base_dir.iterdir():
            if folder.is_dir() and folder.name.startswith(company_number):
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
    """
    Perform OCR on downloaded financial PDFs of a specific company.

    This function scans the downloaded PDFs directory for a folder matching the company number,
    and performs OCR on each PDF to convert them into searchable text files.

    Args:
    company_number (str): The company number whose financials are to be OCRed.
    """
    ocr_processor = OCR(TESSERACT_PATH)
    base_dir = Path("./data/downloaded_pdfs")
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
    """
    Analyze the OCR-processed PDFs of a company to count occurrences of specified search terms.

    This function searches through OCR-processed PDFs for specified terms and generates a CSV
    with the counts of each term per document.

    Args:
    company_number (str): The company number whose PDFs are to be analyzed.
    """
    base_dir = Path("./data/searchable_pdfs")
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


def main():
    """
    Main execution function to manage the workflow of downloading, OCR processing, and analyzing company financials.

    Based on configuration settings, this script manages the sequence of downloading, OCR processing,
    and analyzing financial documents of specified companies.
    """
    limiter = RateLimiter(590, 300)
    if DOWNLOAD_FINANCIALS:
        for number in COMPANY_NUMBERS:
            try:
                logging.info(f"Downloading financials for company {number}")
                download_financials(number, limiter)
            except Exception as e:
                logging.error(f"Error downloading financials for company {number}: {e}")
                continue

    if OCR_PDFS:
        logging.info("Performing OCR on financials")
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
                executor.map(ocr_financials, COMPANY_NUMBERS)
        except Exception as e:
            logging.error(f"Error performing OCR on financials: {e}")

    if ANALYZE_PDFS:
        for number in COMPANY_NUMBERS:
            try:
                logging.info(f"Analyze company {number}")
                analyze_company(number)
            except Exception as e:
                logging.error(f"Error analyzing company {number}: {e}")
                continue

    if not DOWNLOAD_FINANCIALS and not OCR_PDFS and not ANALYZE_PDFS:
        print("No action specified")


if __name__ == "__main__":
    main()
