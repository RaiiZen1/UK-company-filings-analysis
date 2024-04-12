# test_api.py
import pytest
from unittest.mock import patch
from src.api import CompanyAPI


def test_get_company_profile():
    # Setup
    api = CompanyAPI("https://api.example.com", "dummy_api_key")

    # Patch the requests.get method in api.CompanyAPI.get_company_profile
    with patch("src.api.requests.get") as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {
            "company_name": "Test Company",
            "company_number": "12345678",
        }

        # Execute
        response = api.get_company_profile("12345678")

        # Verify
        assert response["company_name"] == "Test Company"
        assert mocked_get.called  # Ensures that the get method was called
