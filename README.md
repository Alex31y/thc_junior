# Catalogue API

A web scraping and API service for parts catalogue data from urparts.com. This project provides a hierarchical REST API for manufacturers, categories, models, and parts data.

## Architecture

The system consists of two main components:
- **Scraper**: Web scraper using Playwright to extract data from urparts.com
- **API**: FastAPI-based REST service providing paginated access to the catalogue data

Data flows through the hierarchy: Manufacturers → Categories → Models → Parts

## Tech Stack

- **Python 3.11**
- **FastAPI** - REST API framework
- **Playwright** - Web scraping
- **SQLAlchemy** - Database ORM with PostgreSQL
- **PostgreSQL** - Database
- **Docker & Docker Compose** - Containerization
- **Poetry** - Python dependency management

## Quick Start

1. **Start the services:**
   ```bash
   docker compose pull
   docker compose down --volumes
   docker compose up --build
   ```

2. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

## API Endpoints

- `GET /manufacturers` - List manufacturers with search and pagination
- `GET /manufacturers/{id}/categories` - List categories for a manufacturer
- `GET /categories/{id}/models` - List models for a category
- `GET /models/{id}/parts` - List parts for a model

All endpoints support:
- `q` parameter for search
- `page` and `per_page` parameters for pagination

## Development

### Prerequisites
- Python 3.11
- Poetry
- Docker & Docker Compose

### Local Setup
```bash
# Install dependencies
poetry install

# Install Playwright browsers
poetry run playwright install

# Run tests
poetry run pytest
```

### Running Components Separately

**Database:**
```bash
docker compose up postgres
```

**Scraper:**
```bash
export DATABASE_URL="postgresql://dnl@localhost/dnl"
poetry run python -m catalogue.scraper
```

**API Server:**
```bash
export DATABASE_URL="postgresql://dnl@localhost/dnl"
poetry run uvicorn catalogue.api:app --reload
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string (default: `postgresql://dnl@postgres/dnl`)

## Debugging Challenge

**For Developer Applicants**: This project contains intentionally introduced bugs for testing purposes. See [DEBUGGING_CHALLENGE.md](DEBUGGING_CHALLENGE.md) for detailed instructions on finding and fixing the bugs, plus documentation requirements.

## Project Structure

```
catalogue/
├── __init__.py
├── api.py              # FastAPI application
├── database.py         # Database models and operations
├── schemas.py          # Pydantic response schemas
└── scraper.py          # Web scraping logic
tests/
└── api_test.py         # API tests
docker-compose.yml      # Service orchestration
Dockerfile              # Container definition
pyproject.toml          # Python project configuration
DEBUGGING_CHALLENGE.md  # Bug hunting instructions for applicants
```