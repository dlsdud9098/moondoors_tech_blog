"""Pytest configuration and fixtures."""
import sys
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.main import app


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
