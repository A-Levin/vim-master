"""Database configuration and connection management."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


# Global engine and session maker
engine: AsyncEngine = create_async_engine(
    settings.get_database_url(),
    # Performance settings for production
    pool_size=20,  # Base pool size
    max_overflow=30,  # Additional connections during high load
    pool_pre_ping=True,  # Check connections before use
    pool_recycle=3600,  # Recycle connections every hour
    echo=settings.is_development,  # SQL logging only in development
    future=True,
)

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    
    Usage with FastAPI:
    ```python
    async def endpoint(db: AsyncSession = Depends(get_database_session)):
        # Use db session
    ```
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions.
    
    Usage:
    ```python
    async with get_session() as db:
        # Use db session
    ```
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_database() -> None:
    """Initialize database connection and create tables if needed."""
    logger.info("Initializing database connection...")
    
    try:
        # Test connection
        async with engine.begin() as conn:
            # You can add table creation logic here if needed
            # await conn.run_sync(Base.metadata.create_all)
            logger.info("Database connection established successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def close_database() -> None:
    """Close database connections."""
    logger.info("Closing database connections...")
    await engine.dispose()
    logger.info("Database connections closed")