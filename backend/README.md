# Moondoors Tech Blog - Backend API

FastAPI-based backend for the Moondoors Tech Blog platform.

## Features

- FastAPI 0.109+ with async support
- Pydantic Settings for configuration management
- pytest with async test support
- Code quality tools: Black, mypy, ruff
- PostgreSQL with SQLAlchemy 2.0+ and Alembic
- Test coverage > 80%

## Requirements

- Python 3.11+
- PostgreSQL 15+
- Virtual environment (venv or similar)

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (includes production)
pip install -r requirements-dev.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 4. Database Setup

```bash
# Run migrations
alembic upgrade head
```

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Run Specific Tests

```bash
# Run specific file
pytest tests/test_health.py

# Run specific test
pytest tests/test_health.py::test_health_endpoint_returns_200

# Run with markers
pytest -m unit
pytest -m integration
```

## Code Quality

### Format Code

```bash
black .
```

### Type Checking

```bash
mypy app
```

### Linting

```bash
ruff check .
```

### Run All Quality Checks

```bash
black --check . && mypy app && ruff check .
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   └── api/                 # API routes
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_health.py       # Health check tests
│   └── ...
├── alembic/                 # Database migrations
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pytest.ini              # Pytest configuration
├── pyproject.toml          # Tool configurations
├── .env.example            # Environment variables template
└── README.md               # This file
```

## API Endpoints

### Health Check

```
GET /health
```

Returns application health status and version.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## Environment Variables

See `.env.example` for required environment variables:

- `APP_NAME`: Application name
- `DEBUG`: Debug mode (true/false)
- `ENVIRONMENT`: Environment (development/staging/production)
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT tokens
- And more...

## Development Workflow

1. Create feature branch
2. Write failing tests (RED)
3. Implement minimum code (GREEN)
4. Refactor and improve (REFACTOR)
5. Run quality checks
6. Commit changes
7. Create pull request

## Contributing

Follow TDD methodology:
1. Write tests first
2. Ensure tests fail
3. Implement minimal code
4. Make tests pass
5. Refactor
6. Commit with conventional commits

## License

MIT License
