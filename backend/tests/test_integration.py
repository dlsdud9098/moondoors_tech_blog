"""Integration tests for database functionality."""
import pytest
from sqlalchemy import text


class TestDatabaseIntegration:
    """Integration tests for full database lifecycle."""

    @pytest.mark.asyncio
    async def test_full_connection_lifecycle(self):
        """Test complete database connection lifecycle."""
        from app.database import get_engine, get_db, init_db, close_db

        # Initialize
        await init_db()

        # Get engine
        engine = get_engine()
        assert engine is not None

        # Test connection
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1 as value"))
            row = result.first()
            assert row is not None
            assert row.value == 1

        # Test session dependency
        async for session in get_db():
            result = await session.execute(text("SELECT 2 as value"))
            row = result.first()
            assert row.value == 2
            break

        # Cleanup
        await close_db()

    @pytest.mark.asyncio
    async def test_transaction_rollback(self):
        """Test that failed transactions are rolled back properly."""
        from app.database import get_db
        import pytest

        try:
            async for session in get_db():
                # Execute valid query
                await session.execute(text("SELECT 1"))

                # Force error
                raise ValueError("Test error")
        except ValueError:
            # Error should be raised
            pass

        # Session should be cleaned up and new sessions should work
        async for session in get_db():
            result = await session.execute(text("SELECT 1"))
            assert result is not None
            break

    @pytest.mark.asyncio
    async def test_connection_pool_reuse(self):
        """Test that connection pool is reused across sessions."""
        from app.database import get_engine

        # Get engine multiple times
        engine1 = get_engine()
        engine2 = get_engine()

        # Should be same instance (singleton pattern)
        assert engine1 is engine2

        # Pool should be configured
        assert engine1.pool is not None

    @pytest.mark.asyncio
    async def test_multiple_concurrent_sessions(self):
        """Test multiple concurrent database sessions."""
        from app.database import get_db
        import asyncio

        results = []

        async def query_database(value: int):
            async for session in get_db():
                result = await session.execute(text(f"SELECT {value} as val"))
                row = result.first()
                results.append(row.val)
                break

        # Run multiple queries concurrently
        await asyncio.gather(
            query_database(1),
            query_database(2),
            query_database(3),
        )

        # All queries should succeed
        assert len(results) == 3
        assert sorted(results) == [1, 2, 3]

    @pytest.mark.asyncio
    async def test_database_url_configuration(self):
        """Test that database URL is properly loaded from configuration."""
        from app.config import get_settings
        from app.database import get_engine

        settings = get_settings()
        engine = get_engine()

        # Engine URL should match configuration
        assert "postgresql+asyncpg" in str(engine.url)
        assert "techblog" in str(engine.url) or "test" in str(engine.url)
