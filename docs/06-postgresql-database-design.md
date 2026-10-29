# Phase 6: PostgreSQL Database Design

## Objective

Create the PostgreSQL table that will store processed daily weather data from the Open-Meteo Historical Weather API.

## Database Setup

The project uses PostgreSQL running in Docker. The weather database is named `weather`, and the application connects using the `weather_user` account.

The connection settings are supplied through environment variables rather than hardcoded credentials.

Inside Docker, the PostgreSQL hostname is `postgres` and the port is `5432`. This hostname works because Docker Compose allows the services to communicate over its internal network.

## Table Design

The table is named `daily_weather` and stores one record per city per date.

| Column | PostgreSQL type | Purpose |
|---|---|---|
| `city` | `TEXT` | City associated with the observation |
| `date` | `DATE` | Date of the weather observation |
| `temperature_2m_mean` | `DOUBLE PRECISION` | Daily mean temperature at 2 metres |
| `temperature_2m_max` | `DOUBLE PRECISION` | Daily maximum temperature |
| `temperature_2m_min` | `DOUBLE PRECISION` | Daily minimum temperature |
| `precipitation_sum` | `DOUBLE PRECISION` | Total daily precipitation |
| `wind_speed_10m_max` | `DOUBLE PRECISION` | Maximum daily wind speed at 10 metres |
| `weather_code` | `INTEGER` | Weather condition code |
| `ingested_at` | `TIMESTAMPTZ` | Timestamp indicating when the record was ingested |

### Data Integrity

The table applies the following constraints:

- `city` and `date` are required fields.
- `ingested_at` is required and has a database-generated default timestamp.
- A unique constraint on `(city, date)` prevents multiple records for the same city and date.

The composite unique constraint is important because each city should have only one daily weather record for a given date. It will also support the upsert operation in Phase 7.

## Schema Implementation

The table definition is maintained in `src/database/schema.sql`.

`CREATE TABLE IF NOT EXISTS` allows the schema setup to run without failing simply because the table already exists. This makes the schema suitable for repeated execution during development and pipeline runs.

The schema was applied from the Airflow scheduler container using the database connection settings supplied by Docker Compose. The operation completed successfully.

The table columns and their PostgreSQL data types were then queried through `information_schema.columns`. The returned columns matched the intended schema.

## Design Decisions

- **PostgreSQL:** Provides a relational database for structured weather records.
- **One row per city per date:** Makes daily weather data straightforward to query and analyse.
- **Composite unique constraint:** Prevents duplicate daily observations and supports reliable repeat loads.
- **`TIMESTAMPTZ` for ingestion time:** Preserves timezone-aware ingestion timestamps.
- **Separate schema file:** Keeps database structure separate from Python application logic.

## Outcome

The `daily_weather` table has been created successfully in PostgreSQL, and its columns and data types have been verified.

The database is ready for Phase 7, where processed weather records will be inserted and updated using an idempotent loading function.

## Docker and Database Commands

Apply the schema from the Airflow scheduler container:

```powershell
docker compose exec airflow-scheduler python -c "import os, psycopg2; from pathlib import Path; c=psycopg2.connect(host=os.environ['WEATHER_DB_HOST'], port=os.environ['WEATHER_DB_PORT'], dbname=os.environ['WEATHER_DB_NAME'], user=os.environ['WEATHER_DB_USER'], password=os.environ['WEATHER_DB_PASSWORD']); c.cursor().execute(Path('/opt/airflow/src/database/schema.sql').read_text()); c.commit(); c.close(); print('Schema applied successfully')"
```

Inspect the table columns and data types:

```powershell
docker compose exec airflow-scheduler python -c "import os, psycopg2; c=psycopg2.connect(host=os.environ['WEATHER_DB_HOST'], port=os.environ['WEATHER_DB_PORT'], dbname=os.environ['WEATHER_DB_NAME'], user=os.environ['WEATHER_DB_USER'], password=os.environ['WEATHER_DB_PASSWORD']); cur=c.cursor(); cur.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position', ('daily_weather',)); print(cur.fetchall()); cur.close(); c.close()"
```

**Note:** These commands document the setup and verification performed during development. They do not need to be rerun unless the schema needs to be reapplied or checked.