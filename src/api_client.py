import requests
from config import API_KEY, BASE_URL


class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (API_KEY, "")

    def get(self, url):
        return self.session.get(url)

    def get_company_profile(self, company_number):
        url = f"{BASE_URL}/company/{company_number}"
        return self.get(url)

    def get_filing_history_page(
        self, company_number, start_index=0, items_per_page=100
    ):
        url = f"{BASE_URL}/company/{company_number}/filing-history?start_index={start_index}&items_per_page={items_per_page}"
        return self.get(url)

    def get_document_metadata(self, url):
        return self.get(url)
