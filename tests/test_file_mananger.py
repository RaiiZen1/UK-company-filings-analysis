# test_file_manager.py

import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.file_manager import FileManager

# Define constants for use in tests
TEST_DIRECTORY = "test_files"
TEST_FILE = "test.pdf"
TEST_URL = "http://example.com/test.pdf"


# Fixture to clean up the created directory after each test
@pytest.fixture
def clean_up_directory():
    yield
    if os.path.exists(TEST_DIRECTORY):
        os.rmdir(TEST_DIRECTORY)


def test_directory_creation(clean_up_directory):
    """
    Test that a directory is created if it doesn't exist when FileManager is initialized.
    """
    if os.path.exists(TEST_DIRECTORY):
        os.rmdir(TEST_DIRECTORY)
    fm = FileManager(TEST_DIRECTORY)
    assert os.path.isdir(TEST_DIRECTORY), "Directory should be created"


@patch("requests.get")
def test_download_pdf(mock_get, clean_up_directory):
    """
    Test that a PDF is downloaded correctly.
    """
    # Set up the mock to return a response with content
    mock_get.return_value.ok = True
    mock_get.return_value.content = b"Test PDF content"

    fm = FileManager(TEST_DIRECTORY)
    fm.download_pdf(TEST_URL, TEST_FILE)

    assert os.path.isfile(
        os.path.join(TEST_DIRECTORY, TEST_FILE)
    ), "File should exist after download"


@patch("requests.get")
def test_download_pdf_exists(mock_get, clean_up_directory):
    """
    Test that download_pdf doesn't download the file if it already exists.
    """
    # Set up a fake file
    open(os.path.join(TEST_DIRECTORY, TEST_FILE), "wb").close()

    fm = FileManager(TEST_DIRECTORY)
    fm.download_pdf(TEST_URL, TEST_FILE)

    # Assert get was not called because the file exists
    mock_get.assert_not_called()


@patch("requests.get")
def test_download_pdf_failure(mock_get, clean_up_directory):
    """
    Test that download_pdf raises an exception on a failed download.
    """
    # Configure the mock to raise an HTTP error
    mock_get.return_value.raise_for_status.side_effect = Exception("Failed to download")

    fm = FileManager(TEST_DIRECTORY)
    with pytest.raises(Exception, match="Failed to download"):
        fm.download_pdf(TEST_URL, TEST_FILE)
