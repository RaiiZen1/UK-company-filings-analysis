import os
import requests
from config import API_KEY, BASE_URL


class FileManager:
    def __init__(self, directory):
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def download_pdf(self, document_url, filename):
        file_path = os.path.join(self.directory, filename)
        if not os.path.exists(file_path):
            # Adding authentication to the request
            response = requests.get(
                document_url, auth=(API_KEY, ""), allow_redirects=True
            )
            if response.status_code == 200:
                with open(file_path, "wb") as pdf_file:
                    pdf_file.write(response.content)
                print(f"PDF downloaded: {filename}")
            else:
                raise Exception(f"Failed to download PDF: {response.status_code}")
        else:
            print(f"File already exists: {filename}")
