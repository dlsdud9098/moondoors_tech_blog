"""Test pytest fixtures configuration."""
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

import pytest


def test_conftest_exists():
    """Test that conftest.py exists."""
    conftest_path = Path(__file__).parent / "conftest.py"
    assert conftest_path.exists(), "conftest.py should exist in tests/"


def test_client_fixture_exists(client):
    """Test that client fixture exists and works."""
    assert client is not None, "client fixture should exist"


@pytest.mark.asyncio
async def test_async_client_fixture_exists(async_client):
    """Test that async_client fixture exists and works."""
    assert async_client is not None, "async_client fixture should exist"


@pytest.mark.asyncio
async def test_async_client_can_make_requests(async_client):
    """Test that async_client can make HTTP requests."""
    response = await async_client.get("/health")
    assert response.status_code == 200, "async_client should be able to make requests"
