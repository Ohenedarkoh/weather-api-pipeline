import json

from src.api.storage import save_raw_weather


def test_save_raw_weather(tmp_path, monkeypatch):
    """Check that API data is saved correctly as JSON."""

    # Make the storage function use a temporary data folder.
    monkeypatch.chdir(tmp_path)

    weather_data = {
        "daily": {
            "time": ["2026-09-01"],
            "temperature_2m_mean": [26.5],
        }
    }

    file_path = save_raw_weather(
        data=weather_data,
        city="Accra",
        start_date="2026-09-01",
        end_date="2026-09-01",
    )

    # Confirm the file was created.
    assert file_path.exists()

    # Read the file and confirm its contents are unchanged.
    with open(file_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == weather_data
    assert file_path.name == "2026-09-01_2026-09-01.json"