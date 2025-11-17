# TDD Plan: PostgreSQL Database Setup and Connection (#2)

## Overview
Set up PostgreSQL database connection using SQLAlchemy 2.0 with async support (asyncpg driver), configure connection pooling, session management, and Alembic migrations.

## Prerequisites
- Issue #1 completed (FastAPI project structure)
- PostgreSQL running in Docker (localhost:5432)
- Python dependencies: SQLAlchemy 2.0, asyncpg, alembic, pytest-asyncio

## TDD Steps

### Step 1: Test Database Connection Configuration
- [x] **RED**: Write test for database URL configuration
- [x] **GREEN**: Implement database URL in config
- [x] **REFACTOR**: Extract configuration logic
- [x] **MARK**: Update progress

### Step 2: Test Async Engine Creation
- [x] **RED**: Write test for SQLAlchemy async engine creation
- [x] **GREEN**: Create async engine with connection pool
- [x] **REFACTOR**: Add proper pool configuration (size=10, max_overflow=20)
- [x] **MARK**: Update progress

### Step 3: Test Database Session Management
- [x] **RED**: Write test for async session creation
- [x] **GREEN**: Implement async_sessionmaker
- [x] **REFACTOR**: Add session lifecycle management
- [x] **MARK**: Update progress

### Step 4: Test Session Dependency Injection
- [x] **RED**: Write test for FastAPI session dependency
- [x] **GREEN**: Implement get_db dependency
- [x] **REFACTOR**: Add proper cleanup and error handling
- [x] **MARK**: Update progress

### Step 5: Test Database Initialization
- [x] **RED**: Write test for database initialization utility
- [x] **GREEN**: Create init_db() and close_db() functions
- [x] **REFACTOR**: Add startup/shutdown event handlers
- [x] **MARK**: Update progress

### Step 6: Test Database Separation (Dev vs Test)
- [x] **RED**: Write test for test database isolation
- [x] **GREEN**: Implement TEST_DATABASE_URL configuration
- [x] **REFACTOR**: Add pytest fixtures for test database
- [x] **MARK**: Update progress

### Step 7: Alembic Migration Setup
- [x] **RED**: Write test for alembic configuration
- [x] **GREEN**: Initialize alembic with async template
- [x] **REFACTOR**: Configure env.py for async migrations
- [x] **MARK**: Update progress

### Step 8: Test Migration Execution
- [x] **RED**: Write test for migration execution
- [x] **GREEN**: Create sample migration
- [x] **REFACTOR**: Document migration commands
- [x] **MARK**: Update progress

### Step 9: Integration Tests
- [x] **RED**: Write end-to-end database connection test
- [x] **GREEN**: Test full connection lifecycle
- [x] **REFACTOR**: Add comprehensive error handling tests
- [x] **MARK**: Update progress

### Step 10: Coverage and Documentation
- [ ] **RED**: Write test for coverage threshold (>80%)
- [ ] **GREEN**: Achieve target coverage
- [ ] **REFACTOR**: Add docstrings and type hints
- [ ] **MARK**: Update progress

## File Structure
```
backend/
├── app/
│   ├── database.py          # Main database module
│   ├── config.py            # Updated with DB config
│   └── models/
│       └── __init__.py      # SQLAlchemy base
├── alembic/
│   ├── env.py              # Alembic async environment
│   ├── script.py.mako      # Migration template
│   └── versions/           # Migrations directory
├── alembic.ini             # Alembic configuration
└── tests/
    ├── conftest.py         # DB test fixtures
    └── test_database.py    # Database tests
```

## Commit Message Format
- `test(#2): add test for [feature]`
- `feat(#2): implement [feature]`
- `refactor(#2): improve [feature]`
- `docs(#2): mark [step] complete`

## Success Criteria
- ✅ All database connection tests pass
- ✅ Connection pool configured correctly
- ✅ Session dependency injection works
- ✅ Dev and test databases separated
- ✅ Alembic migrations functional
- ✅ Test coverage > 80%
- ✅ All completion criteria met

## Notes
- Use SQLAlchemy 2.0 async API
- Async context manager for sessions
- Proper connection cleanup
- Environment-based configuration
- Type hints for all functions
