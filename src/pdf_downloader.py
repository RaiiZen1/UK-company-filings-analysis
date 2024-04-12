import os
import requests
import logging


def download_pdf(url, directory, filename):
    """
    Downloads a PDF from a URL and saves it to a specified directory with a given filename.

    Args:
        url (str): The URL from where to download the PDF.
        directory (str): The local directory to save the downloaded PDF.
        filename (str): The name to save the file as.

    Returns:
        str: Path to the downloaded file if successful, or None if the file exists already.

    Raises:
        IOError: If the download or file saving process fails.
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Complete file path
    file_path = os.path.join(directory, filename)

    # Check if the file already exists
    if os.path.exists(file_path):
        logging.info(f"File already exists: {file_path}")
        return None

    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

        # Write the file to the specified path
        with open(file_path, "wb") as f:
            f.write(response.content)
        logging.info(f"PDF downloaded: {file_path}")
        return file_path
    except requests.RequestException as e:
        logging.error(f"Failed to download PDF due to an HTTPError: {e}")
        raise IOError(f"Failed to download PDF: {e}")
    except Exception as e:
        logging.error(f"Failed to save PDF: {e}")
        raise IOError(f"Failed to save PDF: {e}")


# Set up logging at the appropriate level in your main configuration or entry script
logging.basicConfig(level=logging.INFO)
