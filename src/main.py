from config import COMPANY_NUMBERS
from api_client import APIClient
from rate_limiter import RateLimiter
from file_manager import FileManager


def process_company(company_number):
    client = APIClient()
    limiter = RateLimiter(600, 300)
    manager = FileManager(f"./data/{company_number}")

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


if __name__ == "__main__":
    for number in COMPANY_NUMBERS:
        try:
            process_company(number)
        except Exception as e:
            print(f"Error processing company {number}: {e}")
