import fitz  # PyMuPDF
import logging
import csv
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def search_pdf_and_output_to_csv(pdf_dir_path: str, terms: list, output_csv_path: str):
    """
    Search for a list of terms in all PDFs within a given directory and output the counts to a CSV file.

    Args:
        pdf_dir_path (str): Path to the directory containing PDF files.
        terms (list): List of strings to search for in the PDFs.
        output_csv_path (str): Path to the output CSV file.
    """
    # Create the CSV file if it does not exist and write the header
    if not os.path.exists(output_csv_path):
        with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.DictWriter(
                csvfile, fieldnames=["company_id", "name", "date", "type"] + terms
            )
            csv_writer.writeheader()

    # Iterate over all PDFs in the directory
    for filename in os.listdir(pdf_dir_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir_path, filename)
            company_id = os.path.basename(pdf_dir_path)
            parts = filename.replace(".pdf", "").split("_")
            date_part = parts[1]
            type_part = "_".join(parts[2:])  # join the remaining parts to form the type
            date = datetime.strptime(date_part, "%Y-%m-%d").date()

            # Initialize counts dictionary
            term_counts = {term: 0 for term in terms}

            # Open the PDF
            doc = fitz.open(pdf_path)

            # Iterate over the pages and search for each term
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                for term in terms:
                    # Find instances of the term
                    areas = page.search_for(term)
                    temp = term_counts[term]
                    term_counts[term] += len(areas)  # Count occurrences
                    if temp != term_counts[term]:
                        logging.info(f"Found term '{term}' on page {page_num + 1}")

            # Close the document
            doc.close()

            # Write to CSV
            with open(output_csv_path, "a", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.DictWriter(
                    csvfile, fieldnames=["company_id", "name", "date", "type"] + terms
                )
                row_data = {
                    "company_id": company_id,
                    "name": "N/A",
                    "date": date,
                    "type": type_part,
                    **term_counts,
                }
                csv_writer.writerow(row_data)
            logging.info(f"Data for file {filename} written to {output_csv_path}")
