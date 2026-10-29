import requests
import logging
from pathlib import Path


log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)

# define the log file
filename = log_dir / "client.log"

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    
    # create console handler and set level to info
    ch= logging.StreamHandler()
    ch.setLevel(logging.INFO)

    
    # create file handler and set level to debug
    fh = logging.FileHandler(filename,encoding="utf-8")
    fh.setLevel(logging.DEBUG)


    #create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)



api_url = "https://archive-api.open-meteo.com/v1/archive"

weather_variables = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
    "weather_code",
]




def fetch_weather(latitude,longitude,start_date,end_date):
        """Fetch daily historical weather data from open-meteo"""

        params={
            'latitude':latitude,
            "longitude":longitude,
            "start_date":start_date,
            "end_date":end_date,
            "daily":",".join(weather_variables),
            "timezone":"auto"
        }
        try:
            logger.info("Fetching historical weather data")
            response= requests.get(api_url,params=params,timeout=30)
            response.raise_for_status()

            weather_data = response.json()

            logger.info("Successfully fetched weather data.")
            return weather_data
        except requests.RequestException:
            logger.exception("Failed to fetch weather data")
            raise

        except ValueError:
            logger.exception("Failed to decode the API  response as JSON")
            raise

















# API_KEY = "YOUR_API_KEY"
# city = input("Enter your city: ")
# url = "YOUR_WEATHER_API_URL"
# params = {
#     "q": city,
#     "appid": API_KEY,
#     "units": "metric"
# }
# try:
#     response = requests.get(
#         url,
#         params=params,
#         timeout=10
#     )
#     response.raise_for_status()
#     data = response.json()
#     temperature = data["main"]["temp"]
#     humidity = data["main"]["humidity"]
#     wind_speed = data["wind"]["speed"]
#     condition = data["weather"][0]["description"]
#     print("\n--- WEATHER REPORT ---")
#     print("City:", city)
#     print("Condition:", condition)
#     print("Temperature:", temperature, "°C")
#     print("Humidity:", humidity, "%")
#     print("Wind Speed:", wind_speed, "m/s")
# except requests.exceptions.RequestException:
#     print("Could not connect to the weather service.")
# except KeyError:
#     print("Unexpected weather data received.")









