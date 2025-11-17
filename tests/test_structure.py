"""Test backend project structure exists."""
import os
from pathlib import Path


def test_backend_directory_exists():
    """Test that backend directory exists."""
    backend_path = Path(__file__).parent.parent / "backend"
    assert backend_path.exists(), "backend directory should exist"
    assert backend_path.is_dir(), "backend should be a directory"


def test_app_directory_exists():
    """Test that backend/app directory exists."""
    app_path = Path(__file__).parent.parent / "backend" / "app"
    assert app_path.exists(), "backend/app directory should exist"
    assert app_path.is_dir(), "backend/app should be a directory"


def test_tests_directory_exists():
    """Test that backend/tests directory exists."""
    tests_path = Path(__file__).parent.parent / "backend" / "tests"
    assert tests_path.exists(), "backend/tests directory should exist"
    assert tests_path.is_dir(), "backend/tests should be a directory"


def test_alembic_directory_exists():
    """Test that backend/alembic directory exists."""
    alembic_path = Path(__file__).parent.parent / "backend" / "alembic"
    assert alembic_path.exists(), "backend/alembic directory should exist"
    assert alembic_path.is_dir(), "backend/alembic should be a directory"


def test_init_files_exist():
    """Test that __init__.py files exist in app and tests."""
    base_path = Path(__file__).parent.parent / "backend"

    app_init = base_path / "app" / "__init__.py"
    assert app_init.exists(), "backend/app/__init__.py should exist"

    tests_init = base_path / "tests" / "__init__.py"
    assert tests_init.exists(), "backend/tests/__init__.py should exist"

    api_init = base_path / "app" / "api" / "__init__.py"
    assert api_init.exists(), "backend/app/api/__init__.py should exist"
