import pytest
from unittest.mock import patch, Mock
from src.api_client import APIClient
from src.config import BASE_URL


@pytest.fixture
def api_client():
    return APIClient()


def test_get_company_profile_success(api_client):
    company_number = "12345678"
    expected_url = f"{BASE_URL}/company/{company_number}"

    with patch("src.api_client.requests.Session.get") as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json = Mock(return_value={"company": "test_company"})
        mock_get.return_value = mock_response

        response = api_client.get_company_profile(company_number)
        mock_get.assert_called_once_with(expected_url)
        assert response.json() == {"company": "test_company"}
        assert response.raise_for_status.called


def test_get_company_profile_failure(api_client):
    company_number = "12345678"
    expected_url = f"{BASE_URL}/company/{company_number}"

    with patch("src.api_client.requests.Session.get") as mock_get:
        # Mimic a failed HTTP request by raising a RequestException
        from requests.exceptions import RequestException

        mock_get.side_effect = RequestException("An error occurred")

        response = api_client.get_company_profile(company_number)
        mock_get.assert_called_once_with(expected_url)
        assert response is None
