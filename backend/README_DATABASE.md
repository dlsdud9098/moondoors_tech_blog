# Database Setup Guide

## Overview

This project uses PostgreSQL with SQLAlchemy 2.0 async support for database operations.

## Architecture

- **ORM**: SQLAlchemy 2.0 with async support
- **Driver**: asyncpg
- **Migrations**: Alembic
- **Connection Pool**: Size 10, Max Overflow 20
- **Session Management**: Async context managers with dependency injection

## Quick Start

### 1. Prerequisites

Ensure PostgreSQL is installed and running:

```bash
# Check PostgreSQL status
pg_isready

# Or using Docker
docker compose up -d postgres
```

### 2. Configure Database

Copy `.env.example` to `.env` and update database credentials:

```bash
DATABASE_URL=postgresql+asyncpg://bloguser:blogpassword@localhost:5432/techblog
TEST_DATABASE_URL=postgresql+asyncpg://bloguser:blogpassword@localhost:5432/techblog_test
```

### 3. Create Databases

```bash
# Create main database
createdb techblog

# Create test database
createdb techblog_test
```

Or using psql:

```sql
CREATE DATABASE techblog;
CREATE DATABASE techblog_test;
```

### 4. Run Migrations

```bash
cd backend
alembic upgrade head
```

### 5. Verify Setup

```bash
cd backend
pytest tests/test_database.py -v
```

## Database Structure

```
backend/
├── app/
│   ├── database.py          # Database engine and session management
│   ├── models/              # SQLAlchemy models
│   │   └── __init__.py
│   └── config.py            # Database configuration
├── alembic/
│   ├── env.py              # Alembic async environment
│   ├── script.py.mako      # Migration template
│   └── versions/           # Migration files
├── alembic.ini             # Alembic configuration
└── tests/
    ├── conftest.py         # Test fixtures with DB isolation
    ├── test_database.py    # Database unit tests
    └── test_integration.py # Integration tests
```

## Key Components

### Database Engine (`app/database.py`)

- **get_engine()**: Returns singleton async engine instance
- **get_sessionmaker()**: Returns configured async session maker
- **get_db()**: FastAPI dependency for database sessions
- **init_db()**: Initialize database (create tables)
- **close_db()**: Cleanup database connections

### Configuration (`app/config.py`)

```python
from app.config import get_settings

settings = get_settings()
print(settings.database_url)  # Development database
print(settings.test_database_url)  # Test database
```

### Usage in FastAPI Endpoints

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

@app.get("/items")
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return items
```

### Creating Models

```python
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
```

## Testing

### Running Tests

```bash
# All database tests
pytest tests/test_database.py -v

# Integration tests
pytest tests/test_integration.py -v

# With coverage
pytest tests/test_database.py --cov=app.database --cov-report=html
```

### Test Database Isolation

Tests use separate test database with automatic cleanup:

```python
@pytest.mark.asyncio
async def test_user_creation(test_db_session):
    # test_db_session is automatically isolated
    user = User(email="test@example.com")
    test_db_session.add(user)
    await test_db_session.commit()
    # Database rolled back after test
```

## Migrations

See [MIGRATIONS.md](./MIGRATIONS.md) for detailed migration guide.

### Common Commands

```bash
# Create new migration
alembic revision --autogenerate -m "add user table"

# Apply migrations
alembic upgrade head

# Revert migration
alembic downgrade -1

# View history
alembic history
```

## Connection Pooling

Configured for optimal performance:

- **Pool Size**: 10 connections
- **Max Overflow**: 20 additional connections
- **Pool Pre-ping**: Enabled (checks connection health)
- **Pool Recycle**: 3600 seconds (1 hour)

## Best Practices

1. **Always use async/await** with database operations
2. **Use dependency injection** (`get_db`) in FastAPI endpoints
3. **Write tests** for all database operations
4. **Use transactions** for multi-step operations
5. **Handle errors** gracefully with try/except
6. **Close connections** properly (handled automatically by context managers)

## Troubleshooting

### Connection refused

```bash
# Check PostgreSQL is running
pg_isready

# Check credentials in .env
cat .env | grep DATABASE_URL
```

### Permission denied

```bash
# Grant permissions
psql -c "GRANT ALL PRIVILEGES ON DATABASE techblog TO bloguser;"
```

### Migration conflicts

```bash
# Check current state
alembic current

# View pending migrations
alembic history

# Reset to base (careful!)
alembic downgrade base
alembic upgrade head
```

### Test database issues

```bash
# Recreate test database
dropdb techblog_test
createdb techblog_test

# Or in psql
DROP DATABASE techblog_test;
CREATE DATABASE techblog_test;
```

## Performance Tips

1. Use **select in load** to avoid N+1 queries
2. Add **database indexes** for frequently queried fields
3. Use **connection pooling** (already configured)
4. Monitor **slow queries** with logging
5. Use **database-level constraints** for data integrity

## Security

1. **Never commit** `.env` file with real credentials
2. **Use environment variables** for production
3. **Restrict database user** permissions
4. **Enable SSL** for production database connections
5. **Regularly update** dependencies for security patches

## Resources

- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
- [FastAPI Database Guide](https://fastapi.tiangolo.com/tutorial/sql-databases/)
