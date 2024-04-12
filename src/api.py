import logging
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict


class CompanyAPI:
    """
    Handles communication with the Companies House API to fetch company profiles
    and their filing histories.

    Attributes:
        base_url (str): Base URL for the Companies House API.
        auth (HTTPBasicAuth): Authentication credentials for the API.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the API client with the necessary authentication.

        Args:
            base_url (str): The base URL for the Companies House API.
            api_key (str): API key for authenticating requests.
        """
        self.base_url = base_url
        self.auth = HTTPBasicAuth(api_key, "")

    def get_company_profile(self, company_number: str) -> Dict:
        """
        Retrieve the company profile using the company number.

        Args:
            company_number (str): The unique identifier for the company.

        Returns:
            dict: The company profile as a JSON object.
        """
        url = f"{self.base_url}/company/{company_number}"
        try:
            response = requests.get(url, auth=self.auth, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve company profile: {e}")
            raise

    def get_filing_history(
        self, company_number: str, start_index: int = 0, items_per_page: int = 100
    ) -> Dict:
        """
        Fetch the filing history for a company.

        Args:
            company_number (str): The company number.
            start_index (int): The index of the first record to fetch (pagination).
            items_per_page (int): Number of items to fetch per page.

        Returns:
            dict: A portion of the company's filing history as a JSON object.
        """
        url = f"{self.base_url}/company/{company_number}/filing-history"
        params = {"start_index": start_index, "items_per_page": items_per_page}
        try:
            response = requests.get(url, auth=self.auth, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve filing history: {e}")
            raise


# Configure logging at the beginning of your script
logging.basicConfig(level=logging.INFO)
