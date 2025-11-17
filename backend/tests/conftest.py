"""Pytest configuration and fixtures."""
import os
import sys
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.main import app
from app.config import get_settings
from app.database import Base, get_db


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """Synchronous test client fixture.

    Yields:
        TestClient: FastAPI test client for synchronous tests
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Asynchronous test client fixture.

    Yields:
        AsyncClient: HTTPX async client for async tests
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Get test database URL.

    Returns:
        str: Test database URL from settings
    """
    settings = get_settings()
    return settings.test_database_url


@pytest.fixture(scope="function")
async def test_db_engine(test_database_url: str):
    """Create test database engine.

    Args:
        test_database_url: Test database URL from fixture

    Yields:
        AsyncEngine: Test database engine
    """
    engine = create_async_engine(test_database_url, echo=False)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def test_db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session.

    Args:
        test_db_engine: Test database engine from fixture

    Yields:
        AsyncSession: Test database session
    """
    async_session = sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
def override_get_db(test_db_session: AsyncSession):
    """Override get_db dependency for testing.

    Args:
        test_db_session: Test database session from fixture

    Returns:
        callable: Dependency override function
    """

    async def _override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()
