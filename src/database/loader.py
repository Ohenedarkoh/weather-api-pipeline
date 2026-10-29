import logging
import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv


# Load database credentials and connection settings from .env.
load_dotenv()

logger = logging.getLogger(__name__)


def load_weather_data(df):
    """Load processed weather records into PostgreSQL."""

    # Avoid opening a database connection when there is no data.
    if df.empty:
        logger.info("No weather records to load")
        return

    connection = psycopg2.connect(
        host=os.getenv("WEATHER_DB_HOST", "localhost"),
        port=os.getenv("WEATHER_DB_PORT", "5432"),
        dbname=os.getenv("WEATHER_DB_NAME", "weather"),
        user=os.getenv("WEATHER_DB_USER", "weather_user"),
        password=os.getenv("WEATHER_DB_PASSWORD"),
    )

    try:
        with connection.cursor() as cursor:

            # Apply the schema before inserting records.
            schema_path = Path(__file__).with_name("schema.sql")

            with open(schema_path, "r", encoding="utf-8") as file:
                cursor.execute(file.read())

            # Insert new records or update matching city/date records.
            insert_sql = """
                INSERT INTO daily_weather (
                    city, date,
                    temperature_2m_mean, temperature_2m_max,
                    temperature_2m_min, precipitation_sum,
                    wind_speed_10m_max, weather_code, ingested_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (city, date)
                DO UPDATE SET
                    temperature_2m_mean = EXCLUDED.temperature_2m_mean,
                    temperature_2m_max = EXCLUDED.temperature_2m_max,
                    temperature_2m_min = EXCLUDED.temperature_2m_min,
                    precipitation_sum = EXCLUDED.precipitation_sum,
                    wind_speed_10m_max = EXCLUDED.wind_speed_10m_max,
                    weather_code = EXCLUDED.weather_code,
                    ingested_at = EXCLUDED.ingested_at;
            """

            # Convert DataFrame rows into tuples for the SQL placeholders.
            records = [
                (
                    row.city,
                    row.date,
                    row.temperature_2m_mean,
                    row.temperature_2m_max,
                    row.temperature_2m_min,
                    row.precipitation_sum,
                    row.wind_speed_10m_max,
                    row.weather_code,
                    row.ingested_at.to_pydatetime()
                    if isinstance(row.ingested_at, pd.Timestamp)
                    else row.ingested_at,
                )
                for row in df.itertuples(index=False)
            ]

            # Send all records using the same SQL statement.
            cursor.executemany(insert_sql, records)

        # Save changes only if the entire load succeeds.
        connection.commit()
        logger.info("Loaded %s weather records", len(records))

    except Exception:
        # Undo database changes if any part of the load fails.
        connection.rollback()
        logger.exception("Failed to load weather data")
        raise

    finally:
        # Always release the database connection.
        connection.close()
