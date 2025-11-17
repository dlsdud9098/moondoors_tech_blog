# Database Migrations Guide

This document describes how to use Alembic for database migrations in the Moondoors Tech Blog project.

## Overview

We use Alembic with async SQLAlchemy 2.0 for database schema migrations. All migrations are version-controlled and can be applied/reverted safely.

## Prerequisites

- PostgreSQL database running
- Python dependencies installed (`requirements.txt`, `requirements-dev.txt`)
- Database URL configured in `.env` or environment variables

## Common Commands

### Create a New Migration

Auto-generate migration from model changes:

```bash
cd backend
alembic revision --autogenerate -m "description of changes"
```

Create an empty migration:

```bash
cd backend
alembic revision -m "description of changes"
```

### Apply Migrations

Apply all pending migrations:

```bash
cd backend
alembic upgrade head
```

Apply specific number of migrations:

```bash
cd backend
alembic upgrade +1  # Apply next migration
alembic upgrade +2  # Apply next 2 migrations
```

Apply to specific revision:

```bash
cd backend
alembic upgrade <revision_id>
```

### Revert Migrations

Revert last migration:

```bash
cd backend
alembic downgrade -1
```

Revert to specific revision:

```bash
cd backend
alembic downgrade <revision_id>
```

Revert all migrations:

```bash
cd backend
alembic downgrade base
```

### View Migration History

Show current revision:

```bash
cd backend
alembic current
```

Show migration history:

```bash
cd backend
alembic history
```

Show migration history with details:

```bash
cd backend
alembic history --verbose
```

## Migration File Structure

```
backend/
├── alembic/
│   ├── env.py              # Alembic environment (async configured)
│   ├── script.py.mako      # Migration template
│   └── versions/           # Migration files
│       └── xxxx_description.py
└── alembic.ini             # Alembic configuration
```

## Writing Migrations

### Example Migration File

```python
"""Add user table

Revision ID: abc123
Revises:
Create Date: 2024-01-01 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = 'abc123'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    """Revert migration."""
    op.drop_table('users')
```

## Best Practices

1. **Always review auto-generated migrations** before applying them
2. **Test migrations** on development database first
3. **Write reversible migrations** (implement both upgrade and downgrade)
4. **Use descriptive names** for migration messages
5. **Keep migrations small** and focused on one change
6. **Never modify** existing migration files in production
7. **Backup database** before running migrations in production

## Async Support

Our Alembic configuration supports async SQLAlchemy:

- Uses `async_engine_from_config`
- Runs migrations with `asyncio.run()`
- Compatible with `asyncpg` driver

## Troubleshooting

### Migration fails with "target database has pending migrations"

```bash
# Check current state
alembic current

# View history
alembic history

# Manually mark as applied (use with caution)
alembic stamp head
```

### Auto-generate doesn't detect changes

1. Ensure models are imported in `app/database.py`
2. Verify Base.metadata includes all models
3. Check that database URL is correct

### Async errors during migration

Ensure your environment supports async operations and that `asyncpg` is installed:

```bash
pip install asyncpg
```

## Testing Migrations

Run migrations on test database:

```bash
# Set test database URL
export DATABASE_URL="postgresql+asyncpg://bloguser:blogpassword@localhost:5432/techblog_test"

# Run migrations
alembic upgrade head

# Run tests
pytest

# Revert
alembic downgrade base
```

## CI/CD Integration

In CI/CD pipeline:

```bash
# Run migrations before tests
alembic upgrade head

# Run tests
pytest

# Verify migrations can be reverted
alembic downgrade base
alembic upgrade head
```

## Support

For issues or questions, refer to:
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
