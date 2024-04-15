import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class OCR:
    """
    A class to handle OCR processing of PDF files using PyMuPDF and pytesseract.

    Attributes:
        tesseract_cmd (str): The path to the Tesseract executable.
        language (str): The language for OCR to use.
    """

    def __init__(self, tesseract_cmd: str, language: str = "eng"):
        """
        The constructor for OCR class.

        Parameters:
            tesseract_cmd (str): The path to the Tesseract executable.
            language (str): The language to use for OCR (default is English).
        """
        self.tesseract_cmd = tesseract_cmd
        self.language = language
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
        logging.info(
            "OCR class instantiated with Tesseract command: %s", self.tesseract_cmd
        )

    def list_files_in_directory(self, directory: str) -> List[str]:
        """
        Lists all files in a given directory.

        Parameters:
            directory (str): The directory path to list files from.

        Returns:
            List[str]: A list of file names found in the directory.
        """
        files = os.listdir(directory)
        # logging.info("Files in directory '%s': %s", directory, files)
        return files

    def perform_ocr_on_pdf(self, pdf_path: str, output_path: str):
        """
        Performs OCR on a PDF file and creates a searchable PDF with the recognized text.

        Parameters:
            pdf_path (str): The path to the PDF file to perform OCR on.
            output_path (str): The path where the searchable PDF will be saved.
        """
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            logging.error("Error opening PDF file at %s: %s", pdf_path, e)
            return

        # Check if the PDF already exists
        if os.path.exists(output_path):
            logging.info("Searchable PDF already exists: %s", output_path)
            return

        logging.info("Performing OCR on: %s", pdf_path)
        for page_number in range(len(doc)):
            page = doc.load_page(page_number)  # get page
            pix = page.get_pixmap()  # render page to an image
            img = Image.open(
                io.BytesIO(pix.tobytes())
            )  # convert the image to PIL format

            # Perform OCR using pytesseract
            text = pytesseract.image_to_string(img, lang=self.language)

            # Create a text layer in the PDF
            rc = page.search_for(text)  # find position of text
            if not rc:  # if text not already there
                page.insert_text((0, 0), text, fontsize=11, overlay=True)

        # Save the modified PDF
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            doc.save(output_path)
            logging.info("Saved searchable PDF to: %s", output_path)
        except Exception as e:
            logging.error("Error saving searchable PDF to %s: %s", output_path, e)
