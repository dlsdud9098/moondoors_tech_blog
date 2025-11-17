"""Database connection and session management."""
from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.config import get_settings

# SQLAlchemy Base for models
Base = declarative_base()

# Global engine instance
_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Get or create the async database engine.

    Returns:
        AsyncEngine: SQLAlchemy async engine with connection pooling
    """
    global _engine

    if _engine is None:
        settings = get_settings()

        _engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """Get or create the async session maker.

    Returns:
        async_sessionmaker: SQLAlchemy async session maker
    """
    global _sessionmaker

    if _sessionmaker is None:
        engine = get_engine()
        _sessionmaker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    return _sessionmaker


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency for FastAPI.

    Yields:
        AsyncSession: Database session that automatically commits/rollbacks
    """
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database connection.

    Creates all tables if they don't exist.
    """
    engine = get_engine()

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connection.

    Disposes the engine and cleans up connection pool.
    """
    global _engine, _sessionmaker

    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _sessionmaker = None
