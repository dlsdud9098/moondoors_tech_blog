"""Test health check endpoint."""
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint_exists():
    """Test that /health endpoint exists."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code != 404, "/health endpoint should exist"


@pytest.mark.asyncio
async def test_health_endpoint_returns_200():
    """Test that /health endpoint returns 200 OK."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200, "/health should return 200 OK"


@pytest.mark.asyncio
async def test_health_endpoint_returns_json():
    """Test that /health endpoint returns JSON."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.headers["content-type"] == "application/json"


@pytest.mark.asyncio
async def test_health_endpoint_response_format():
    """Test that /health endpoint returns expected format."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        data = response.json()

        assert "status" in data, "Response should have 'status' field"
        assert data["status"] == "healthy", "Status should be 'healthy'"
        assert "version" in data, "Response should have 'version' field"


@pytest.mark.asyncio
async def test_health_endpoint_always_available():
    """Test that /health endpoint is always available (no auth required)."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Multiple calls should all succeed
        for _ in range(3):
            response = await client.get("/health")
            assert response.status_code == 200
