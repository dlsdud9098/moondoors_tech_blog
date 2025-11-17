"""Tests for database connection and configuration."""
import pytest


class TestDatabaseConfiguration:
    """Test database configuration settings."""

    def test_database_url_configuration(self):
        """Test that database URL is properly configured."""
        from app.config import get_settings

        settings = get_settings()

        # Verify database URL exists and has correct format
        assert settings.database_url is not None
        assert "postgresql+asyncpg://" in settings.database_url

        # Verify database URL components
        assert "bloguser" in settings.database_url
        assert "techblog" in settings.database_url

    def test_test_database_url_configuration(self):
        """Test that test database URL is separate from development database."""
        from app.config import get_settings

        settings = get_settings()

        # Test database should have different name
        assert hasattr(settings, "test_database_url")
        assert settings.test_database_url is not None
        assert "test_" in settings.test_database_url or "_test" in settings.test_database_url

        # Test and dev databases should be different
        assert settings.test_database_url != settings.database_url
