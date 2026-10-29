
import json
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def save_raw_weather(data, city, start_date, end_date):
    """Save the original weather API response as a JSON file."""

    output_directory = Path("data/raw") / city.lower()
    file_path = output_directory / f"{start_date}_{end_date}.json"

    try:
        output_directory.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        logger.info("Raw weather data saved to %s", file_path)
        return file_path

    except (OSError, TypeError, ValueError):
        logger.exception("Failed to save raw weather data for %s", city)
        raise
