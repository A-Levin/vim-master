"""Tests for database configuration and connection management."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from app.config.database import (
    get_database_session,
    get_session,
    init_database,
    close_database,
    Base,
)


class TestDatabaseConnection:
    """Test database connection management."""

    @pytest.mark.asyncio
    async def test_get_database_session_success(self, test_session):
        """Test successful database session creation."""
        # Mock the session factory
        with patch('app.config.database.async_session_factory') as mock_factory:
            mock_factory.return_value.__aenter__.return_value = test_session
            mock_factory.return_value.__aexit__.return_value = None
            
            async for session in get_database_session():
                assert isinstance(session, AsyncSession)
                break

    @pytest.mark.asyncio
    async def test_get_database_session_exception_rollback(self):
        """Test database session rollback on exception."""
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit.side_effect = Exception("Database error")
        
        with patch('app.config.database.async_session_factory') as mock_factory:
            mock_factory.return_value.__aenter__.return_value = mock_session
            mock_factory.return_value.__aexit__.return_value = None
            
            with pytest.raises(Exception, match="Database error"):
                async for session in get_database_session():
                    await session.commit()  # This will raise
                    break
            
            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_session_context_manager(self, test_session):
        """Test get_session context manager."""
        with patch('app.config.database.async_session_factory') as mock_factory:
            mock_factory.return_value.__aenter__.return_value = test_session
            mock_factory.return_value.__aexit__.return_value = None
            
            async with get_session() as session:
                assert isinstance(session, AsyncSession)

    @pytest.mark.asyncio
    async def test_get_session_exception_handling(self):
        """Test get_session exception handling."""
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit.side_effect = Exception("Database error")
        
        with patch('app.config.database.async_session_factory') as mock_factory:
            mock_factory.return_value.__aenter__.return_value = mock_session
            mock_factory.return_value.__aexit__.return_value = None
            
            with pytest.raises(Exception, match="Database error"):
                async with get_session() as session:
                    raise Exception("Database error")
            
            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_init_database_success(self):
        """Test successful database initialization."""
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_conn = AsyncMock()
        mock_engine.begin.return_value.__aenter__.return_value = mock_conn
        
        with patch('app.config.database.engine', mock_engine):
            with patch('app.config.database.logger') as mock_logger:
                await init_database()
                
                mock_engine.begin.assert_called_once()
                mock_logger.info.assert_any_call("Initializing database connection...")
                mock_logger.info.assert_any_call("Database connection established successfully")

    @pytest.mark.asyncio
    async def test_init_database_failure(self):
        """Test database initialization failure."""
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_engine.begin.side_effect = Exception("Connection failed")
        
        with patch('app.config.database.engine', mock_engine):
            with patch('app.config.database.logger') as mock_logger:
                with pytest.raises(Exception, match="Connection failed"):
                    await init_database()
                
                mock_logger.error.assert_called_once_with(
                    "Failed to initialize database: Connection failed"
                )

    @pytest.mark.asyncio
    async def test_close_database(self):
        """Test database connection closing."""
        mock_engine = AsyncMock(spec=AsyncEngine)
        
        with patch('app.config.database.engine', mock_engine):
            with patch('app.config.database.logger') as mock_logger:
                await close_database()
                
                mock_engine.dispose.assert_called_once()
                mock_logger.info.assert_any_call("Closing database connections...")
                mock_logger.info.assert_any_call("Database connections closed")


class TestBase:
    """Test Base model class."""

    def test_base_model_exists(self):
        """Test Base model class exists and is properly configured."""
        assert Base is not None
        assert hasattr(Base, 'metadata')
        assert hasattr(Base, 'registry')