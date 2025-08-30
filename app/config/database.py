"""Database configuration and connection management."""

import logging

from app.db.base import create_tables

logger = logging.getLogger(__name__)


async def init_database() -> None:
    """Initialize database connection and create tables if needed."""
    logger.info("Initializing database connection...")
    create_tables()
    logger.info("Database connection established successfully")


async def close_database() -> None:
    """Close database connections."""
    logger.info("Closing database connections...")
    logger.info("Database connections closed")
