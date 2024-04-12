import logging
from api import CompanyAPI
from pdf_downloader import download_pdf
from dotenv import load_dotenv
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from .env file
load_dotenv()

# Constants
BASE_URL = "https://api.companieshouse.gov.uk"
API_KEY = os.getenv("COMPANY_API_KEY")

if API_KEY is None:
    logging.error(
        "API_KEY is not set. Please set the COMPANY_API_KEY environment variable in the .env file."
    )
    sys.exit(1)


def fetch_and_download(company_number):
    api_client = CompanyAPI(BASE_URL, API_KEY)
    try:
        company_profile = api_client.get_company_profile(company_number)
        logging.info(f"Company Profile: {company_profile}")

        filing_history = api_client.get_filing_history(company_number)
        for filing in filing_history["items"]:
            if "document_metadata" in filing["links"]:
                document_url = filing["links"]["document_metadata"]
                filename = f"{filing['date']}_accounts.pdf"
                download_pdf(document_url, "./data", filename)
    except Exception as e:
        logging.error(
            f"An error occurred while processing company number {company_number}: {e}"
        )


def main():
    company_number = (
        "01087941"  # Example company number, replace with dynamic input as needed
    )
    fetch_and_download(company_number)


if __name__ == "__main__":
    main()
