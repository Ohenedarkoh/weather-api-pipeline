#mocking means replacing a real dependency with a controlled substitute during a test
#mock creates a fake api response
#patch temporarily replace requests.get() so the test does not contact the real API


from unittest.mock import Mock, patch

from src.api.client import fetch_weather

import requests
import pytest


@patch("src.api.client.requests.get")
def test_fetch_weather_success(mock_get):
    expected_data = {
        "daily": {
            "time": ["2026-09-01"],
            "temperature_2m_mean": [26.5],
        }
    }

    # Create a fake response and configure its JSON data
    mock_response = Mock()
    mock_response.json.return_value = expected_data

    # Make the fake request return our fake response
    mock_get.return_value = mock_response

    # Call the actual function we want to test
    result = fetch_weather(
        latitude=5.6037,
        longitude=-0.1870,
        start_date="2026-09-01",
        end_date="2026-09-01",
    )

    # Check that the returned data matches what we expected
    assert result == expected_data

    # Check that a request was made exactly once
    mock_get.assert_called_once()

    # Check that HTTP status validation was performed
    mock_response.raise_for_status.assert_called_once()


@patch("src.api.client.requests.get")
def test_fetch_weather_http_error(mock_get):
    """Check that HTTP errors are logged and re-raised."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "API request failed"
    )
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        fetch_weather(
            latitude=5.6037,
            longitude=-0.1870,
            start_date="2026-09-01",
            end_date="2026-09-01",
        )


@patch("src.api.client.requests.get")
def test_fetch_weather_timeout(mock_get):
    """Check that connection timeouts are re-raised."""
    mock_get.side_effect = requests.Timeout("Connection timed out")

    with pytest.raises(requests.Timeout):
        fetch_weather(
            latitude=5.6037,
            longitude=-0.1870,
            start_date="2026-09-01",
            end_date="2026-09-01",
        )