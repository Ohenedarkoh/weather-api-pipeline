
from datetime import datetime, timezone

import pandas as pd


# These are the weather fields expected from the API.
WEATHER_COLUMNS = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
    "weather_code",
]


def process_weather_data(data, city):
    """Convert daily API arrays into one record per city and date."""

    # Check that the API response contains daily weather data.
    if "daily" not in data:
        raise ValueError("API response is missing daily weather data")

    daily_data = data["daily"]

    if "time" not in daily_data:
        raise ValueError("Daily data is missing dates")

    # Confirm that all six expected weather variables are present.
    missing_columns = [
        column for column in WEATHER_COLUMNS
        if column not in daily_data
    ]

    if missing_columns:
        raise ValueError(
            f"Missing weather variables: {missing_columns}"
        )

    # Build a table from the parallel arrays.
    # Pandas matches values by their position in each array.
    records = {"date": daily_data["time"]}

    for column in WEATHER_COLUMNS:
        records[column] = daily_data[column]

    df = pd.DataFrame(records)

    # Add the city and the time this data was processed.
    df["city"] = city
    df["ingested_at"] = datetime.now(timezone.utc)

    # Convert dates to proper date values and weather fields to numbers.
    df["date"] = pd.to_datetime(df["date"], errors="raise").dt.date

    numeric_columns = [
        "temperature_2m_mean",
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "wind_speed_10m_max",
        "weather_code",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="raise")

    # Reject duplicate city/date records before loading.
    if df.duplicated(subset=["city", "date"]).any():
        raise ValueError("Duplicate city/date records found")

    # Reject records without a city or date.
    if df["city"].isna().any() or df["date"].isna().any():
        raise ValueError("City and date must not be missing")

    # Ensure temperature minimum does not exceed maximum.
    invalid_temperatures = (
        df["temperature_2m_min"] > df["temperature_2m_max"]
    )

    if invalid_temperatures.any():
        raise ValueError("Minimum temperature exceeds maximum")

    # Return columns in a predictable order.
    return df[
        [
            "city",
            "date",
            *WEATHER_COLUMNS,
            "ingested_at",
        ]
    ]
