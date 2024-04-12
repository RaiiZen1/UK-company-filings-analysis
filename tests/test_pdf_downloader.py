# test_pdf_downloader.py
import pytest
from unittest.mock import patch, mock_open
from src.pdf_downloader import download_pdf


@patch("src.pdf_downloader.os.path.exists")
@patch("src.pdf_downloader.open", new_callable=mock_open)
@patch("src.pdf_downloader.requests.get")
def test_download_pdf_exists(mocked_get, mocked_open, mocked_exists):
    # Setup
    mocked_exists.return_value = True

    # Execute
    download_pdf("http://example.com/file.pdf", "/fake/directory", "file.pdf")

    # Verify
    mocked_get.assert_not_called()  # Ensures the file is not downloaded again
