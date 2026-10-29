from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.database.loader import load_weather_data


def test_load_weather_data_empty_dataframe():
    # An empty DataFrame should not require a database connection.
    df = pd.DataFrame()

    with patch("src.database.loader.psycopg2.connect") as mock_connect:
        load_weather_data(df)

    # Confirm that no connection was opened.
    mock_connect.assert_not_called()


@patch("src.database.loader.psycopg2.connect")
def test_load_weather_data_success(mock_connect):
    # Prepare a fake database connection and cursor.
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Create one processed weather record.
    df = pd.DataFrame([
        {
            "city": "Accra",
            "date": pd.Timestamp("2026-09-01").date(),
            "temperature_2m_mean": 26.5,
            "temperature_2m_max": 29.1,
            "temperature_2m_min": 24.0,
            "precipitation_sum": 0.0,
            "wind_speed_10m_max": 18.2,
            "weather_code": 2,
            "ingested_at": pd.Timestamp(
                "2026-09-01T12:00:00Z"
            ),
        }
    ])

    # Run the loader using the mocked database.
    load_weather_data(df)

    # Confirm that SQL was executed and changes were committed.
    mock_cursor.execute.assert_called_once()
    mock_cursor.executemany.assert_called_once()
    mock_connection.commit.assert_called_once()
    mock_connection.close.assert_called_once()


@patch("src.database.loader.psycopg2.connect")
def test_load_weather_data_rolls_back_on_failure(mock_connect):
    # Set up a fake database connection that fails during SQL execution.
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    # Supply a non-empty DataFrame to trigger the database operations.
    df = pd.DataFrame([{"city": "Accra"}])

    # Confirm that the failure is raised and the transaction is rolled back.
    with pytest.raises(Exception, match="Database error"):
        load_weather_data(df)

    mock_connection.rollback.assert_called_once()
    mock_connection.close.assert_called_once()
