"""Test FastAPI application instance."""
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))


def test_app_module_exists():
    """Test that app.main module exists."""
    try:
        from app import main
        assert main is not None
    except ImportError as e:
        assert False, f"app.main module should be importable: {e}"


def test_app_instance_exists():
    """Test that FastAPI app instance exists."""
    try:
        from app.main import app
        assert app is not None, "app instance should exist"
    except ImportError as e:
        assert False, f"Could not import app: {e}"


def test_app_is_fastapi_instance():
    """Test that app is a FastAPI instance."""
    try:
        from fastapi import FastAPI
        from app.main import app
        assert isinstance(app, FastAPI), "app should be a FastAPI instance"
    except ImportError as e:
        assert False, f"Could not verify app type: {e}"


def test_app_has_title():
    """Test that app has a title."""
    try:
        from app.main import app
        assert hasattr(app, "title"), "app should have title attribute"
        assert app.title, "app title should not be empty"
    except ImportError as e:
        assert False, f"Could not check app title: {e}"


def test_app_has_version():
    """Test that app has a version."""
    try:
        from app.main import app
        assert hasattr(app, "version"), "app should have version attribute"
        assert app.version, "app version should not be empty"
    except ImportError as e:
        assert False, f"Could not check app version: {e}"
