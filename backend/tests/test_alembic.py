"""Tests for Alembic migration configuration."""
import pytest
from pathlib import Path


class TestAlembicConfiguration:
    """Test Alembic configuration and setup."""

    def test_alembic_ini_exists(self):
        """Test that alembic.ini configuration file exists."""
        backend_dir = Path(__file__).parent.parent
        alembic_ini = backend_dir / "alembic.ini"

        assert alembic_ini.exists()
        assert alembic_ini.is_file()

    def test_alembic_directory_exists(self):
        """Test that alembic directory exists."""
        backend_dir = Path(__file__).parent.parent
        alembic_dir = backend_dir / "alembic"

        assert alembic_dir.exists()
        assert alembic_dir.is_dir()

    def test_alembic_env_exists(self):
        """Test that alembic env.py exists."""
        backend_dir = Path(__file__).parent.parent
        env_py = backend_dir / "alembic" / "env.py"

        assert env_py.exists()
        assert env_py.is_file()

    def test_alembic_env_has_async_support(self):
        """Test that alembic env.py has async support."""
        backend_dir = Path(__file__).parent.parent
        env_py = backend_dir / "alembic" / "env.py"

        content = env_py.read_text()

        # Check for async support
        assert "async def run_async_migrations" in content
        assert "async_engine_from_config" in content
        assert "asyncio" in content

    def test_alembic_versions_directory_exists(self):
        """Test that alembic versions directory exists."""
        backend_dir = Path(__file__).parent.parent
        versions_dir = backend_dir / "alembic" / "versions"

        assert versions_dir.exists()
        assert versions_dir.is_dir()

    def test_alembic_script_template_exists(self):
        """Test that alembic script template exists."""
        backend_dir = Path(__file__).parent.parent
        script_mako = backend_dir / "alembic" / "script.py.mako"

        assert script_mako.exists()
        assert script_mako.is_file()

    def test_alembic_config_imports_models(self):
        """Test that alembic env.py imports Base from models."""
        backend_dir = Path(__file__).parent.parent
        env_py = backend_dir / "alembic" / "env.py"

        content = env_py.read_text()

        # Check that Base is imported
        assert "from app.database import Base" in content
        assert "target_metadata = Base.metadata" in content
