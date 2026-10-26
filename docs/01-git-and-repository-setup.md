# Phase 1: Git and Repository Setup

## 1. Objective

Establish a clean, maintainable Git repository for the `weather-api-pipeline` project. This phase defines the repository structure, version control workflow, and rules for excluding local data, logs, and sensitive configuration.

No API ingestion or pipeline implementation is included in this phase.

## 2. Project Repository

**Repository name:** `weather-api-pipeline`

**Version control:** Git and GitHub

**Default branch:** `develop`

The `develop` branch is the current default branch and will serve as the integration branch during development. A separate `main` branch will be established for the stable release before project completion.

## 3. Initial Project Structure

```text
weather-api-pipeline/
├── dags/
├── src/
│   ├── api/
│   └── database/
├── tests/
├── docs/
├── data/
│   └── raw/
├── logs/
├── README.md
├── requirements.txt
└── .gitignore
```

### Directory responsibilities

- `dags/`: Apache Airflow DAG definitions and workflow orchestration.
- `src/api/`: API request and ingestion functionality.
- `src/database/`: PostgreSQL loading and database-related functionality.
- `tests/`: Automated tests for pipeline components.
- `docs/`: Phase documentation, design decisions, and operational instructions.
- `data/raw/`: Original JSON API responses retained for traceability and potential reprocessing.
- `logs/`: Local pipeline logs.
- `requirements.txt`: Python project dependencies.
- `README.md`: Project overview, architecture, setup instructions, and usage.

The structure separates orchestration, API ingestion, and database operations to make the project easier to understand, test, and maintain.

## 4. Git Workflow

The project follows a feature-branch workflow:

1. Create a feature branch from `develop`.
2. Implement one clearly defined task or phase.
3. Commit changes using descriptive conventional commit messages.
4. Merge the feature branch into `develop`.
5. Test and resolve issues on `develop`.
6. Merge the tested project into `main` for the final release.

The `main` branch will represent the stable, portfolio-ready version. Feature branches may be retained after merging for development history.

### Commit message convention

Commit messages use a conventional prefix followed by a concise description.

Examples:

- `chore: initialize weather API pipeline project`
- `feat: add weather API extraction`
- `test: add API response validation tests`
- `docs: document Docker setup`

## 5. `.gitignore` Configuration

The `.gitignore` file excludes files that should remain local to the development environment.

Key exclusions include:

- `.env` files containing configuration or credentials.
- `.venv/` and Python cache files.
- Local raw data under `data/`.
- Local logs under `logs/`.
- Pytest cache files.

An `.env.example` file may be committed later to document required environment variables without exposing actual credentials.

Raw API data is excluded by default to keep the repository manageable. A small, sanitized sample may be added separately if it is useful for demonstrating the expected response format.

## 6. Repository and Security Principles

- Do not commit passwords, API keys, or database credentials.
- Do not commit virtual environments or generated cache files.
- Keep local raw data and logs out of version control.
- Use descriptive branches and commits.
- Test changes before merging them into the stable release branch.
- Keep project documentation aligned with the actual implementation.

## 7. Phase Completion Criteria

Phase 1 is complete when:

- The local Git repository is initialized.
- The initial directory structure is established.
- `.gitignore` is configured.
- The GitHub remote is connected.
- The initial project structure is committed and pushed to `develop`.
- The branch workflow is established.
- This phase documentation is saved in `docs/`.

## 8. Outcome

The project has a defined repository structure and version control strategy. This provides the foundation for API exploration, ingestion development, PostgreSQL integration, Airflow orchestration, and Docker containerization in subsequent phases.
