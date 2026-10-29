# Phase 4: API Ingestion Logic

## Objective

Build the Python components responsible for retrieving historical weather data from the Open-Meteo API and storing the original response as a raw JSON file.

## Components

### 1. API client — `src/api/client.py`

The API client contains the `fetch_weather()` function.

Its responsibilities are to:
- Send a request to the Open-Meteo historical weather endpoint.
- Pass the latitude, longitude, start date, end date, requested weather variables, and timezone as parameters.
- Check the HTTP response using `raise_for_status()`.
- Decode the response as JSON and return the data.
- Log successful requests and errors.
- Re-raise request and JSON decoding errors so calling code can handle failures.

The request uses a timeout to prevent the program from waiting indefinitely for a response.

### 2. Raw data storage — `src/api/storage.py`

The `save_raw_weather()` function saves the original API response without transforming its contents.

Files are organized by city and requested date range. For example:

`data/raw/accra/2026-09-01_2026-09-03.json`

The function creates the required directory if it does not exist, writes formatted JSON, logs successful saves, and re-raises file or serialization errors.

Raw storage preserves the source response so it can be inspected or processed again later.

### 3. Logging and error handling

The API client uses Python's logging module to report successful requests and failures. Logs are written to the console and a log file.

The storage module uses the same logging system through a module-level logger.

Expected errors are logged with their traceback and re-raised. This allows failures to remain visible rather than being silently ignored.

### 4. Automated tests

The tests are located in:

- `tests/test_api_client.py`
- `tests/test_api_storage.py`

The API client tests use mocks so they do not depend on a live internet connection. They cover:
- Successful API responses.
- HTTP errors.
- Request timeouts.

The storage test uses a temporary directory to verify that the JSON file is created and its contents match the supplied data.

### 5. API connectivity limitation

During development, requests to the historical API endpoint timed out from Python and command-line tools, although the endpoint returned JSON in a browser. The forecast endpoint was reachable from Python during testing.

The precise cause of the historical endpoint connection issue was not confirmed. Mocked tests verify application behavior but do not establish that live historical ingestion works successfully.

A live API request and raw-file save must therefore be verified when connectivity permits.

## Phase outcome

The API client, raw JSON storage function, logging, error handling, and focused automated tests have been implemented.

The four focused tests passed during development. Live historical API connectivity remains a separate verification item.
