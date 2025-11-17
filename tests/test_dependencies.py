"""Test that required dependencies can be imported."""
import sys
from pathlib import Path


def test_requirements_files_exist():
    """Test that requirements files exist."""
    backend_path = Path(__file__).parent.parent / "backend"

    req_file = backend_path / "requirements.txt"
    assert req_file.exists(), "requirements.txt should exist"

    dev_req_file = backend_path / "requirements-dev.txt"
    assert dev_req_file.exists(), "requirements-dev.txt should exist"


def test_fastapi_import():
    """Test that FastAPI can be imported."""
    try:
        import fastapi
        assert fastapi.__version__ >= "0.109.0", "FastAPI version should be 0.109+"
    except ImportError:
        assert False, "FastAPI should be importable"


def test_uvicorn_import():
    """Test that uvicorn can be imported."""
    try:
        import uvicorn
        assert hasattr(uvicorn, "run"), "uvicorn should have run function"
    except ImportError:
        assert False, "uvicorn should be importable"


def test_pydantic_settings_import():
    """Test that pydantic-settings can be imported."""
    try:
        from pydantic_settings import BaseSettings
        assert BaseSettings is not None
    except ImportError:
        assert False, "pydantic-settings should be importable"


def test_pytest_import():
    """Test that pytest can be imported."""
    try:
        import pytest
        assert pytest is not None
    except ImportError:
        assert False, "pytest should be importable"


def test_pytest_asyncio_import():
    """Test that pytest-asyncio can be imported."""
    try:
        import pytest_asyncio
        assert pytest_asyncio is not None
    except ImportError:
        assert False, "pytest-asyncio should be importable"
