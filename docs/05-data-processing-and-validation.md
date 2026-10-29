# Phase 5: Data Processing and Validation

## Objective

Convert the raw Open-Meteo daily response into structured records that can be loaded into PostgreSQL.

## Processing module

The processing logic is implemented in `src/processing.py` through the `process_weather_data()` function.

The function accepts:
- The decoded API response.
- The city associated with the response.

It returns a pandas DataFrame containing one record per city and date.

## Transformation steps

### 1. Validate the response structure

The function checks that the response contains daily data, a date field, and all six expected weather variables.

If required data is missing, the function raises a `ValueError` rather than continuing with an incomplete dataset.

### 2. Convert daily arrays into records

The API returns dates and weather measurements as parallel arrays. The processing function combines the values at matching positions into rows.

Each row represents one day's weather for one city.

### 3. Add metadata

Two additional columns are created:

- `city`: identifies the city associated with the observations.
- `ingested_at`: records when the data was processed, using a UTC-aware timestamp.

### 4. Convert data types

The date column is converted to Python date values. Weather measurements and weather codes are converted to numeric types.

This makes the data more suitable for database storage and analysis.

### 5. Validate records

The function checks for:
- Duplicate records with the same city and date.
- Missing city or date values.
- Minimum temperatures greater than maximum temperatures.

Invalid data raises an error before it reaches the database.

### 6. Return a consistent schema

The function returns the city, date, six weather variables, and ingestion timestamp in a predictable column order.

This provides a consistent interface between processing and database loading.

## Automated tests

Tests are located in `tests/test_processing.py`.

They cover:
- Processing a valid two-day weather response.
- Confirming the output row count, city, dates, measurements, and ingestion timestamps.
- Rejecting an API response that is missing required weather variables.

The tests use sample data rather than making live API requests.

## Design decisions

- **Pandas:** used to structure and transform the daily data clearly.
- **Separate processing module:** keeps transformation logic independent of API requests and database operations.
- **Fail-fast validation:** invalid data is rejected before loading.
- **UTC timestamps:** provide a consistent reference for processing time.
- **City and date identification:** supports the intended database uniqueness rule of one record per city per date.

## Phase outcome

The processing function and two focused automated tests have been implemented. The tests passed during development.

The next phase defines the PostgreSQL schema that will store the processed records.
