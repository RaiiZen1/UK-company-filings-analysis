import requests
import logging
from typing import Optional
from src.config import API_KEY, BASE_URL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COMPANY_PROFILE_ENDPOINT = "/company/{company_number}"
FILING_HISTORY_ENDPOINT = "/company/{company_number}/filing-history"


class APIClient:
    """
    APIClient facilitates communication with the REST API.

    It handles the creation of a session and provides convenience methods
    for making GET requests to the API for different endpoints.
    """

    def __init__(self):
        """
        Initialize the APIClient instance with an authenticated session.
        """
        self.session = requests.Session()
        self.session.auth = (API_KEY, "")

    def get(self, url: str) -> Optional[requests.Response]:
        """
        Make a GET request to a given URL using the authenticated session.

        Args:
            url (str): The URL to which the GET request is made.

        Returns:
            requests.Response: The response object from the API call.
            None: If there is a RequestException during the API call.
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def get_company_profile(self, company_number: str) -> Optional[requests.Response]:
        """
        Retrieve the company profile for a given company number.

        Args:
            company_number (str): The unique identifier for the company.

        Returns:
            requests.Response: The response from the API containing the company profile.
        """
        url = f"{BASE_URL}{COMPANY_PROFILE_ENDPOINT.format(company_number=company_number)}"
        return self.get(url)

    def get_filing_history_page(
        self, company_number: str, start_index: int = 0, items_per_page: int = 100
    ) -> Optional[requests.Response]:
        """
        Retrieve a page of the filing history for a given company number.

        Args:
            company_number (str): The unique identifier for the company.
            start_index (int): The index to start the page at.
            items_per_page (int): The number of items to include on the page.

        Returns:
            requests.Response: The response from the API containing the filing history page.
        """
        url = f"{BASE_URL}{FILING_HISTORY_ENDPOINT.format(company_number=company_number)}?start_index={start_index}&items_per_page={items_per_page}"
        return self.get(url)

    def get_document_metadata(self, url: str) -> Optional[requests.Response]:
        """
        Retrieve the document metadata from a given URL.

        Args:
            url (str): The URL to fetch the document metadata from.

        Returns:
            requests.Response: The response from the API containing the document metadata.
        """
        return self.get(url)
