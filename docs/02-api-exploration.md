# Phase 2: API Exploration and Data Understanding

## 1. Objective

Explore the Open-Meteo Historical Weather API, understand how to construct API requests, inspect the JSON response, and verify the weather variables required for the pipeline before implementation.

## 2. Data Source

- **API:** Open-Meteo Historical Weather API
- **Documentation:** https://open-meteo.com/en/docs/historical-weather-api
- **Endpoint:** `https://archive-api.open-meteo.com/v1/archive`
- **Response format:** JSON
- **Target cities:** Accra, Kumasi, and Tamale, Ghana

## 3. API Request Structure

An API request consists of an endpoint and parameters.

The endpoint identifies the API resource. Query parameters specify the data requested.

Example request tested during exploration:

`https://archive-api.open-meteo.com/v1/archive?latitude=5.56&longitude=-0.20&start_date=2025-01-01&end_date=2025-01-03&daily=temperature_2m_max&timezone=Africa%2FAccra`

The request includes:

- `latitude` and `longitude`: approximate coordinates for the requested location.
- `start_date` and `end_date`: the historical period.
- `daily`: the weather variable requested.
- `timezone`: the timezone used for daily timestamps.

The request returned a JSON response successfully.

## 4. Response Structure

The response contains location metadata, units, and daily weather data.

Important fields include:

- `latitude` and `longitude`: coordinates associated with the returned data.
- `daily_units`: units for the daily measurements.
- `daily.time`: dates corresponding to the daily measurements.
- `daily.temperature_2m_max`: maximum temperatures for those dates.

Daily measurements are returned as separate arrays aligned by position. The ingestion process must match each date with its corresponding measurement when preparing individual daily records.

The coordinates returned by the API may differ slightly from the coordinates supplied in the request because weather data is associated with grid points.

## 5. Planned Daily Variables

The following six variables were selected and checked against the official API documentation:

| Variable | Description |
|---|---|
| `temperature_2m_mean` | Daily mean temperature at 2 metres |
| `temperature_2m_max` | Daily maximum temperature |
| `temperature_2m_min` | Daily minimum temperature |
| `precipitation_sum` | Total daily precipitation |
| `wind_speed_10m_max` | Maximum daily wind speed at 10 metres |
| `weather_code` | Code representing weather conditions |

These variables will be requested together in the daily parameter rather than through separate requests for each measurement.

## 6. Historical Date Range and Data Availability

The initial project design uses a configurable 30-day historical period.

Historical datasets can have different publication delays. Therefore, the pipeline should not assume that the latest dates are complete. The selected date range should account for the availability of the chosen data source.

The date range will be configurable to support future backfills without changing the ingestion logic.

Official documentation: https://open-meteo.com/en/docs/historical-weather-api

## 7. Project Design Decisions

- Use Python to retrieve and process API responses.
- Preserve original JSON responses in raw storage.
- Extract daily measurements and align them with their dates.
- Include city identification and an ingestion timestamp in prepared records.
- Load the prepared records into PostgreSQL.
- Use Apache Airflow to orchestrate the pipeline.
- Use Docker Compose to run the project services.
- Keep transformations minimal and implement idempotent database loading in later phases.

## 8. Phase Outcome

The endpoint, query parameters, response format, location coordinates, date-range parameters, and required daily variables have been explored.

The project is ready to move from API exploration into implementation planning and environment setup.

