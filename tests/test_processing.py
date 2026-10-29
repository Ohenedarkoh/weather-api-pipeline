
import pandas as pd
import pytest

from src.processing import process_weather_data


def test_process_weather_data():
    # Create sample API data with two days of weather measurements.
    # This avoids needing a live API connection during testing.
    data = {
        "daily": {
            "time": ["2026-09-01", "2026-09-02"],
            "temperature_2m_mean": [26.5, 26.6],
            "temperature_2m_max": [29.1, 29.3],
            "temperature_2m_min": [24.0, 24.1],
            "precipitation_sum": [0.0, 2.4],
            "wind_speed_10m_max": [18.2, 16.7],
            "weather_code": [2, 61],
        }
    }

    # Process the sample data as if it came from Accra.
    df = process_weather_data(data, "Accra")

    # Confirm that each input date becomes one output row.
    assert len(df) == 2

    # Confirm that the city is added to every record.
    assert df["city"].tolist() == ["Accra", "Accra"]

    # Confirm that the dates are converted to Python date values.
    assert df["date"].tolist() == [
        pd.Timestamp("2026-09-01").date(),
        pd.Timestamp("2026-09-02").date(),
    ]

    # Confirm that the weather measurements are preserved.
    assert df["temperature_2m_mean"].tolist() == [26.5, 26.6]
    assert df["weather_code"].tolist() == [2, 61]

    # Confirm that every record has an ingestion timestamp.
    assert df["ingested_at"].notna().all()


def test_process_weather_data_rejects_missing_variable():
    # Create deliberately incomplete data: most required weather
    # variables are missing.
    data = {
        "daily": {
            "time": ["2026-09-01"],
            "temperature_2m_mean": [26.5],
        }
    }

    # The function should raise ValueError instead of processing
    # incomplete data as if it were valid.
    with pytest.raises(ValueError, match="Missing weather variables"):
        process_weather_data(data, "Accra")
