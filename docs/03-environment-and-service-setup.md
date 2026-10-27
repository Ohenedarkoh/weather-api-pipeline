# Phase 3: Environment and Service Setup

## Objective

Set up a reproducible local development environment using Docker Compose, PostgreSQL, and Apache Airflow.

## Tools and Dependencies

- Python and a local virtual environment for development and testing.
- Docker Desktop with the WSL 2 backend.
- Docker Compose for managing the application services.
- PostgreSQL 16 for the Airflow metadata database and weather data.
- Apache Airflow 3.3.2 for workflow orchestration.
- Python dependencies: `requests`, `psycopg2-binary`, `python-dotenv`, and `pytest`.

Airflow runs inside Docker rather than the local Python virtual environment.

## Services and Architecture

Docker Compose manages four main services:

- **PostgreSQL:** Stores Airflow metadata and the weather database.
- **Airflow API server:** Provides the Airflow web interface and API.
- **Airflow scheduler:** Schedules and triggers workflows.
- **Airflow DAG processor:** Parses DAG files so Airflow can discover workflows.

The Airflow services share a custom image built from the project's Dockerfile.

## Database Configuration

The PostgreSQL container initializes an Airflow database and user. The initialization script also creates a separate `weather` database owned by `weather_user`.

The weather database is the target for pipeline data. The Airflow database stores orchestration metadata.

The initialization script runs automatically only when PostgreSQL initializes a new, empty data directory. Existing database volumes are preserved between container restarts.

Database credentials and Airflow configuration values are stored in `.env`, which is excluded from Git. `.env.example` documents the required variables without exposing real credentials.

## Authentication

Airflow uses its Simple Auth Manager. The administrator username is configured through the environment, and Airflow generates the login password automatically.

The generated password must be kept private. It should not be committed to the repository.

## Docker Commands Used

Build the custom Airflow image:

```powershell
docker build -t weather-api-airflow:latest .
```

Validate the Compose configuration:

```powershell
docker compose config --quiet
```

Initialize the Airflow metadata database:

```powershell
docker compose up airflow-init
```

Start the services:

```powershell
docker compose up -d
```

Check service status and health:

```powershell
docker compose ps
```

View API server logs:

```powershell
docker compose logs airflow-apiserver
```

Follow API server logs live:

```powershell
docker compose logs -f airflow-apiserver
```

Stop the services without deleting persistent database data:

```powershell
docker compose down
```

Rebuild the image after changing dependencies or the Dockerfile:

```powershell
docker build -t weather-api-airflow:latest .
docker compose up -d
```

The API server is exposed at `http://localhost:8081` because port `8080` was already occupied on the host computer.

**Warning:** `docker compose down -v` removes named volumes and can delete persisted database data. It should not be used for routine shutdowns.

## Verification

The environment was verified by confirming that:

- The PostgreSQL service reached a healthy state.
- Airflow metadata database migrations completed.
- The Airflow API server started successfully.
- The scheduler and DAG processor started successfully.
- The Airflow interface was accessible through the browser.

## Outcome

The local orchestration and database environment is ready for development of the weather ingestion pipeline.
