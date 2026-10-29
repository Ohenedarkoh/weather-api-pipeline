
from src.api.client import fetch_weather
from src.api.storage import save_raw_weather


data = fetch_weather(
    latitude=5.6037,
    longitude=-0.1870,
    start_date="2026-09-01",
    end_date="2026-09-03",
)

file_path = save_raw_weather(
    data=data,
    city='Accra',
    start_date='2026-09-01',
    end_date='2026-09-03'
)

print(f'Raw weather data saved to:{file_path}')
