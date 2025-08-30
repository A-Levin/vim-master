"""Pytest configuration and fixtures for VimMaster tests."""

import asyncio
from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram import Bot
from aiogram.types import Chat, Message, User
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from app.config.database import Base
from app.config.settings import Settings

# Import app only when needed to avoid bot initialization issues


# Test settings
@pytest.fixture
def test_settings() -> Settings:
    """Test settings with overrides."""
    return Settings(
        debug=True,
        telegram_bot_token="123456:TEST_TOKEN",
        database_url="sqlite+aiosqlite:///:memory:",
        redis_url="redis://localhost:6379/15",  # Test database
        secret_key="test-secret-key",
        log_level="DEBUG",
    )


# Database fixtures
@pytest.fixture
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async with AsyncSession(test_engine, expire_on_commit=False) as session:
        yield session
        await session.rollback()


# Bot fixtures
@pytest.fixture
def mock_bot() -> Bot:
    """Mock bot instance."""
    bot = MagicMock(spec=Bot)
    bot.session = AsyncMock()
    return bot


@pytest.fixture
def test_user() -> User:
    """Test user fixture."""
    return User(
        id=12345,
        is_bot=False,
        first_name="Test",
        last_name="User",
        username="testuser",
        language_code="en",
    )


@pytest.fixture
def test_chat() -> Chat:
    """Test chat fixture."""
    return Chat(
        id=-12345,
        type="private",
        title="Test Chat",
        username="testchat",
        first_name="Test",
        last_name="Chat",
    )


@pytest.fixture
def test_message(test_user: User, test_chat: Chat) -> Message:
    """Test message fixture."""
    return Message(
        message_id=1,
        from_user=test_user,
        chat=test_chat,
        date=1234567890,
        text="/start",
    )


# API fixtures
@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """Test client for FastAPI."""
    # Import here to avoid initialization issues
    from app.main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Async test client for FastAPI."""
    # Import here to avoid initialization issues
    from app.main import app

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


# Mock fixtures for external services
@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    redis_mock = AsyncMock()
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    redis_mock.delete.return_value = 1
    redis_mock.ping.return_value = True
    return redis_mock


# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Utility functions for tests
@pytest.fixture
def make_message():
    """Factory for creating test messages."""

    def _make_message(
        text: str = "/start",
        user_id: int = 12345,
        chat_id: int = 12345,
        username: str = "testuser",
        first_name: str = "Test",
    ) -> Message:
        user = User(
            id=user_id,
            is_bot=False,
            first_name=first_name,
            username=username,
        )
        chat = Chat(id=chat_id, type="private")
        return Message(
            message_id=1,
            from_user=user,
            chat=chat,
            date=1234567890,
            text=text,
        )

    return _make_message


@pytest.fixture
def make_callback_query():
    """Factory for creating test callback queries."""

    def _make_callback_query(
        data: str = "test",
        user_id: int = 12345,
        username: str = "testuser",
    ):
        from aiogram.types import CallbackQuery

        user = User(
            id=user_id,
            is_bot=False,
            first_name="Test",
            username=username,
        )

        # Create a mock message for the callback
        message = Message(
            message_id=1,
            from_user=user,
            chat=Chat(id=user_id, type="private"),
            date=1234567890,
            text="Test message",
        )

        return CallbackQuery(
            id="test_callback",
            from_user=user,
            chat_instance="test_instance",
            data=data,
            message=message,
        )

    return _make_callback_query
