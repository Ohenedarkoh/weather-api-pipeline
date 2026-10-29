# Phase 7: Database Loading

## Objective

Implement the database loading component that transfers processed weather records into the PostgreSQL `daily_weather` table.

The loader receives a processed Pandas DataFrame from the processing module and inserts its records into PostgreSQL.

## Implementation

The loading logic is maintained in:

`src/database/loader.py`

The `load_weather_data()` function handles the database loading process.

Its main responsibilities are:

1. **Database connection:** Connects to PostgreSQL using environment variables.
2. **Schema preparation:** Executes `schema.sql` to ensure the target table exists.
3. **Record preparation:** Converts the DataFrame rows into tuples suitable for PostgreSQL insertion.
4. **Data insertion:** Uses `executemany()` to insert multiple records in one database operation.
5. **Conflict handling:** Uses PostgreSQL's `ON CONFLICT` clause to update existing records.
6. **Transaction management:** Commits successful loads and rolls back failed operations.
7. **Connection cleanup:** Closes the database connection after the operation.

## Upsert Strategy

The table has a unique constraint on `(city, date)`, established in Phase 6.

The loader uses:

```sql
ON CONFLICT (city, date)
DO UPDATE SET
    temperature_2m_mean = EXCLUDED.temperature_2m_mean,
    temperature_2m_max = EXCLUDED.temperature_2m_max,
    temperature_2m_min = EXCLUDED.temperature_2m_min,
    precipitation_sum = EXCLUDED.precipitation_sum,
    wind_speed_10m_max = EXCLUDED.wind_speed_10m_max,
    weather_code = EXCLUDED.weather_code,
    ingested_at = EXCLUDED.ingested_at;
```

This is an **upsert** operation:

- If the city/date combination does not exist, a new record is inserted.
- If it already exists, the existing weather values are updated.

This makes the loading process idempotent: rerunning the same data does not create duplicate city/date records.

## Transaction Management

The loader uses a database transaction to protect the operation.

- `commit()` saves the changes when loading succeeds.
- `rollback()` reverses the transaction if an error occurs.
- `close()` releases the database connection.

This prevents a failed load from leaving partially committed changes.

## Handling Empty Data

If the DataFrame is empty, the loader logs that there are no records to load and returns without opening a database connection.

This avoids unnecessary database operations.

## Testing

The loader is tested in `tests/test_database_loader.py`.

The tests cover:

- Empty DataFrame: verifies that no database connection is opened.
- Successful loading: verifies schema execution, record insertion, transaction commit, and connection closure.
- Loading failure: verifies that the transaction is rolled back and the connection is closed.

The tests use mocked database connections, allowing the loading logic to be tested without depending on a running PostgreSQL instance.

## Configuration

The loader reads its connection settings from environment variables:

- `WEATHER_DB_HOST`
- `WEATHER_DB_PORT`
- `WEATHER_DB_NAME`
- `WEATHER_DB_USER`
- `WEATHER_DB_PASSWORD`

Within Docker Compose, the PostgreSQL service is addressed using the hostname `postgres` and port `5432`.

Credentials are kept outside the source code in the environment configuration.

## Outcome

The database loading component is designed to insert new weather records and update existing city/date records safely.

The next step is to verify the loader against the running PostgreSQL database, then integrate ingestion, processing, and loading into the Airflow workflow.