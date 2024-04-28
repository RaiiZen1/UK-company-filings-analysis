import os
import logging
import requests
from src.config import API_KEY
from src.rate_limiter import RateLimiter

# Configure logging at the top of your module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class FileManager:
    """
    FileManager is responsible for handling file operations, including
    creating directories and downloading files.
    """

    def __init__(self, directory, rate_limiter: RateLimiter):
        """
        Initialize FileManager with a specific directory. Ensure the directory exists.

        :param directory: Directory path where files will be stored.
        """
        self.directory = directory
        self.rate_limiter = rate_limiter
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Directory created or exists: {directory}")

    def download_pdf(self, document_url, filename):
        """
        Download a PDF from a given URL to the specified filename within the directory.

        :param document_url: URL of the PDF to download.
        :param filename: Name of the file to save the PDF as.
        :raises Exception: Raises an exception if the PDF cannot be downloaded.
        """
        file_path = os.path.join(self.directory, filename)
        if not os.path.exists(file_path):
            try:
                self.rate_limiter.check()  # Enforce rate limiting before making a request
                response = requests.get(
                    document_url, auth=(API_KEY, ""), allow_redirects=True
                )
                response.raise_for_status()
                with open(file_path, "wb") as pdf_file:
                    pdf_file.write(response.content)
                logging.info(f"PDF downloaded: {filename}")
            except requests.exceptions.HTTPError as http_err:
                logging.error(f"HTTP error occurred: {http_err}")
                raise
            except requests.exceptions.RequestException as err:
                logging.error(f"Error occurred: {err}")
                raise
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                raise
        else:
            logging.info(f"File already exists: {filename}")
