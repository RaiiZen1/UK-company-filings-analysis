# test_file_manager.py

import os
import pytest
import shutil
from unittest.mock import patch, mock_open, MagicMock
from src.file_manager import FileManager

# Define constants for use in tests
TEST_DIRECTORY = "test_files"
TEST_FILE = "test.pdf"
TEST_URL = "http://example.com/test.pdf"


# Fixture to provide a FileManager with a mocked RateLimiter
@pytest.fixture
def file_manager_with_mocked_rate_limiter(clean_up_directory):
    rate_limiter = MagicMock()  # Create a MagicMock object for the RateLimiter
    fm = FileManager(TEST_DIRECTORY, rate_limiter)
    return fm


# Fixture to clean up the created directory after each test
@pytest.fixture
def clean_up_directory():
    # The directory is created before each test runs
    if not os.path.exists(TEST_DIRECTORY):
        os.makedirs(TEST_DIRECTORY)
    yield
    # The directory is removed after each test runs
    if os.path.exists(TEST_DIRECTORY):
        shutil.rmtree(TEST_DIRECTORY)


@patch("requests.get")
def test_download_pdf(
    mock_get, clean_up_directory, file_manager_with_mocked_rate_limiter
):
    """
    Test that a PDF is downloaded correctly.
    """
    # Set up the mock to return a response with content
    mock_get.return_value.ok = True
    mock_get.return_value.content = b"Test PDF content"

    file_manager_with_mocked_rate_limiter.download_pdf(TEST_URL, TEST_FILE)

    assert os.path.isfile(
        os.path.join(TEST_DIRECTORY, TEST_FILE)
    ), "File should exist after download"


@patch("requests.get")
def test_download_pdf_exists(
    mock_get, clean_up_directory, file_manager_with_mocked_rate_limiter
):
    """
    Test that download_pdf doesn't download the file if it already exists.
    """
    file_path = os.path.join(TEST_DIRECTORY, TEST_FILE)
    # Set up a fake file
    with open(file_path, "wb") as f:
        f.write(b"")

    file_manager_with_mocked_rate_limiter.download_pdf(TEST_URL, TEST_FILE)

    # Assert get was not called because the file exists
    mock_get.assert_not_called()


@patch("requests.get")
def test_download_pdf_failure(
    mock_get, clean_up_directory, file_manager_with_mocked_rate_limiter
):
    """
    Test that download_pdf raises an exception on a failed download.
    """
    # Configure the mock to raise an HTTP error
    mock_get.return_value.raise_for_status.side_effect = Exception("Failed to download")

    with pytest.raises(Exception, match="Failed to download"):
        file_manager_with_mocked_rate_limiter.download_pdf(TEST_URL, TEST_FILE)
