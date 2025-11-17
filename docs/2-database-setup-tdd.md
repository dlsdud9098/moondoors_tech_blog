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
- [ ] **RED**: Write test for async session creation
- [ ] **GREEN**: Implement async_sessionmaker
- [ ] **REFACTOR**: Add session lifecycle management
- [ ] **MARK**: Update progress

### Step 4: Test Session Dependency Injection
- [ ] **RED**: Write test for FastAPI session dependency
- [ ] **GREEN**: Implement get_db dependency
- [ ] **REFACTOR**: Add proper cleanup and error handling
- [ ] **MARK**: Update progress

### Step 5: Test Database Initialization
- [ ] **RED**: Write test for database initialization utility
- [ ] **GREEN**: Create init_db() and close_db() functions
- [ ] **REFACTOR**: Add startup/shutdown event handlers
- [ ] **MARK**: Update progress

### Step 6: Test Database Separation (Dev vs Test)
- [ ] **RED**: Write test for test database isolation
- [ ] **GREEN**: Implement TEST_DATABASE_URL configuration
- [ ] **REFACTOR**: Add pytest fixtures for test database
- [ ] **MARK**: Update progress

### Step 7: Alembic Migration Setup
- [ ] **RED**: Write test for alembic configuration
- [ ] **GREEN**: Initialize alembic with async template
- [ ] **REFACTOR**: Configure env.py for async migrations
- [ ] **MARK**: Update progress

### Step 8: Test Migration Execution
- [ ] **RED**: Write test for migration execution
- [ ] **GREEN**: Create sample migration
- [ ] **REFACTOR**: Document migration commands
- [ ] **MARK**: Update progress

### Step 9: Integration Tests
- [ ] **RED**: Write end-to-end database connection test
- [ ] **GREEN**: Test full connection lifecycle
- [ ] **REFACTOR**: Add comprehensive error handling tests
- [ ] **MARK**: Update progress

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
