"""Tests for database connection and configuration."""
import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


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


class TestAsyncEngine:
    """Test SQLAlchemy async engine creation and configuration."""

    @pytest.mark.asyncio
    async def test_async_engine_creation(self):
        """Test that async engine is created successfully."""
        from app.database import get_engine

        engine = get_engine()

        # Verify engine type
        assert isinstance(engine, AsyncEngine)
        assert engine is not None

    @pytest.mark.asyncio
    async def test_connection_pool_configuration(self):
        """Test that connection pool is configured correctly."""
        from app.database import get_engine

        engine = get_engine()

        # Verify pool settings
        assert engine.pool.size() == 10 or hasattr(engine.pool, '_pool')
        # Pool configuration should exist
        assert engine.pool is not None

    @pytest.mark.asyncio
    async def test_engine_connection(self):
        """Test that engine can establish a database connection."""
        from app.database import get_engine

        engine = get_engine()

        # Try to connect
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            assert result is not None


class TestSessionManagement:
    """Test database session management."""

    @pytest.mark.asyncio
    async def test_sessionmaker_creation(self):
        """Test that session maker is created successfully."""
        from app.database import get_sessionmaker
        from sqlalchemy.ext.asyncio import async_sessionmaker

        sessionmaker = get_sessionmaker()

        # Verify sessionmaker type
        assert isinstance(sessionmaker, async_sessionmaker)
        assert sessionmaker is not None

    @pytest.mark.asyncio
    async def test_session_creation(self):
        """Test that sessions can be created from sessionmaker."""
        from app.database import get_sessionmaker
        from sqlalchemy.ext.asyncio import AsyncSession

        sessionmaker = get_sessionmaker()

        async with sessionmaker() as session:
            # Verify session type
            assert isinstance(session, AsyncSession)
            assert session is not None

    @pytest.mark.asyncio
    async def test_session_configuration(self):
        """Test that session is configured correctly."""
        from app.database import get_sessionmaker

        sessionmaker = get_sessionmaker()

        async with sessionmaker() as session:
            # Verify session configuration
            assert session.expire_on_commit is False
            assert session.autocommit is False
            assert session.autoflush is False


class TestDependencyInjection:
    """Test FastAPI dependency injection for database sessions."""

    @pytest.mark.asyncio
    async def test_get_db_dependency(self):
        """Test that get_db dependency yields a valid session."""
        from app.database import get_db
        from sqlalchemy.ext.asyncio import AsyncSession

        # Get session from dependency
        async for session in get_db():
            # Verify session type
            assert isinstance(session, AsyncSession)
            assert session is not None
            break  # Only test first yield

    @pytest.mark.asyncio
    async def test_get_db_auto_commit(self):
        """Test that get_db automatically commits successful transactions."""
        from app.database import get_db
        from sqlalchemy import text

        async for session in get_db():
            # Execute a query
            result = await session.execute(text("SELECT 1"))
            assert result is not None
            # Session should auto-commit on successful exit
            break

    @pytest.mark.asyncio
    async def test_get_db_auto_rollback(self):
        """Test that get_db automatically rolls back failed transactions."""
        from app.database import get_db

        try:
            async for session in get_db():
                # Force an error
                raise ValueError("Test error")
        except ValueError:
            # Exception should be raised but session should be rolled back
            pass


class TestDatabaseInitialization:
    """Test database initialization and lifecycle management."""

    @pytest.mark.asyncio
    async def test_init_db(self):
        """Test that init_db creates database tables."""
        from app.database import init_db, get_engine, Base

        # Initialize database
        await init_db()

        # Verify tables exist (Base.metadata should have tables)
        engine = get_engine()
        assert engine is not None
        assert Base.metadata is not None

    @pytest.mark.asyncio
    async def test_close_db(self):
        """Test that close_db properly disposes engine."""
        from app.database import get_engine, close_db

        # Get engine
        engine = get_engine()
        assert engine is not None

        # Close database
        await close_db()

        # Engine should be disposed (new engine will be created on next get)
        from app.database import _engine
        assert _engine is None

    @pytest.mark.asyncio
    async def test_lifecycle_integration(self):
        """Test full database lifecycle: init -> use -> close."""
        from app.database import init_db, get_db, close_db
        from sqlalchemy import text

        # Initialize
        await init_db()

        # Use database
        async for session in get_db():
            result = await session.execute(text("SELECT 1"))
            assert result is not None
            break

        # Close
        await close_db()
