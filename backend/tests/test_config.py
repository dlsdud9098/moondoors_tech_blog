"""Test application configuration."""
import sys
from pathlib import Path
import os

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

import pytest


def test_config_module_exists():
    """Test that config module exists."""
    try:
        from app import config
        assert config is not None
    except ImportError as e:
        assert False, f"app.config module should exist: {e}"


def test_settings_class_exists():
    """Test that Settings class exists."""
    try:
        from app.config import Settings
        assert Settings is not None
    except ImportError as e:
        assert False, f"Settings class should exist: {e}"


def test_settings_is_base_settings():
    """Test that Settings inherits from BaseSettings."""
    try:
        from pydantic_settings import BaseSettings
        from app.config import Settings

        assert issubclass(Settings, BaseSettings), "Settings should inherit from BaseSettings"
    except ImportError as e:
        assert False, f"Could not verify Settings inheritance: {e}"


def test_settings_has_required_fields():
    """Test that Settings has required configuration fields."""
    try:
        from app.config import Settings

        # Create instance with minimal config
        settings = Settings()

        # Check required fields exist
        assert hasattr(settings, "app_name"), "Settings should have app_name field"
        assert hasattr(settings, "debug"), "Settings should have debug field"
        assert hasattr(settings, "environment"), "Settings should have environment field"
    except Exception as e:
        assert False, f"Settings should have required fields: {e}"


def test_settings_loads_from_env():
    """Test that Settings loads values from environment variables."""
    try:
        from app.config import Settings

        # Set environment variable
        os.environ["APP_NAME"] = "Test App"
        os.environ["DEBUG"] = "true"

        settings = Settings()
        assert settings.app_name == "Test App", "Settings should load APP_NAME from env"

        # Clean up
        del os.environ["APP_NAME"]
        del os.environ["DEBUG"]
    except Exception as e:
        # Clean up on error
        os.environ.pop("APP_NAME", None)
        os.environ.pop("DEBUG", None)
        assert False, f"Settings should load from environment: {e}"


def test_get_settings_function_exists():
    """Test that get_settings function exists."""
    try:
        from app.config import get_settings
        assert callable(get_settings), "get_settings should be a function"
    except ImportError as e:
        assert False, f"get_settings function should exist: {e}"


def test_get_settings_returns_settings_instance():
    """Test that get_settings returns Settings instance."""
    try:
        from app.config import get_settings, Settings

        settings = get_settings()
        assert isinstance(settings, Settings), "get_settings should return Settings instance"
    except Exception as e:
        assert False, f"get_settings should return Settings instance: {e}"
