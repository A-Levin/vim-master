"""Tests for bot handlers."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.types import Message, CallbackQuery, User, Chat

from app.bot.handlers.start import start_handler, help_handler, profile_handler
from app.bot.handlers.menu import (
    quests_menu_handler,
    learning_menu_handler,
    profile_menu_handler,
    leaderboard_handler,
    help_menu_handler,
    main_menu_callback,
    start_quest_callback,
)


class TestStartHandler:
    """Test start command handler."""

    @pytest.mark.asyncio
    async def test_start_handler_success(self, test_message, make_message):
        """Test successful /start command handling."""
        message = make_message(
            text="/start",
            user_id=12345,
            username="testuser",
            first_name="John"
        )
        message.answer = AsyncMock()
        
        await start_handler(message)
        
        # Verify message was sent
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        # Check message content
        assert "VimMaster" in call_args[0][0]
        assert "John" in call_args[0][0]
        assert "Добро пожаловать" in call_args[0][0]
        
        # Check message parameters
        assert call_args[1]["parse_mode"] == "HTML"
        assert "reply_markup" in call_args[1]

    @pytest.mark.asyncio
    async def test_start_handler_no_user(self):
        """Test start handler with no user in message."""
        message = MagicMock(spec=Message)
        message.from_user = None
        
        # Should return early without calling answer
        await start_handler(message)
        assert not hasattr(message, 'answer') or not message.answer.called

    @pytest.mark.asyncio
    async def test_help_handler(self, make_message):
        """Test /help command handler."""
        message = make_message(text="/help")
        message.answer = AsyncMock()
        
        await help_handler(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        # Check help content
        assert "Помощь по VimMaster" in call_args[0][0]
        assert "/start" in call_args[0][0]
        assert "/help" in call_args[0][0]
        assert call_args[1]["parse_mode"] == "HTML"

    @pytest.mark.asyncio
    async def test_profile_handler(self, make_message):
        """Test /profile command handler."""
        message = make_message(
            text="/profile",
            user_id=12345,
            username="testuser",
            first_name="John"
        )
        message.answer = AsyncMock()
        
        await profile_handler(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        # Check profile content
        assert "Профиль игрока" in call_args[0][0]
        assert "John" in call_args[0][0]
        assert "@testuser" in call_args[0][0]
        assert "12345" in call_args[0][0]
        assert call_args[1]["parse_mode"] == "HTML"

    @pytest.mark.asyncio
    async def test_profile_handler_no_user(self):
        """Test profile handler with no user."""
        message = MagicMock(spec=Message)
        message.from_user = None
        
        await profile_handler(message)
        assert not hasattr(message, 'answer') or not message.answer.called


class TestMenuHandlers:
    """Test menu navigation handlers."""

    @pytest.mark.asyncio
    async def test_quests_menu_handler(self, make_message):
        """Test quests menu handler."""
        message = make_message(text="🎯 Квесты")
        message.answer = AsyncMock()
        
        await quests_menu_handler(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        assert "Квесты и задания" in call_args[0][0]
        assert "reply_markup" in call_args[1]
        assert call_args[1]["parse_mode"] == "HTML"

    @pytest.mark.asyncio
    async def test_learning_menu_handler(self, make_message):
        """Test learning menu handler."""
        message = make_message(text="📚 Обучение")
        message.answer = AsyncMock()
        
        await learning_menu_handler(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        assert "Материалы для обучения" in call_args[0][0]
        assert "Основы Vim" in call_args[0][0]
        assert call_args[1]["parse_mode"] == "HTML"

    @pytest.mark.asyncio
    async def test_profile_menu_handler(self, make_message):
        """Test profile menu handler."""
        message = make_message(
            text="👤 Профиль",
            first_name="Alice",
            username="alice"
        )
        message.answer = AsyncMock()
        
        await profile_menu_handler(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        assert "Профиль игрока" in call_args[0][0]
        assert "Alice" in call_args[0][0]
        assert "@alice" in call_args[0][0]
        assert call_args[1]["parse_mode"] == "HTML"

    @pytest.mark.asyncio
    async def test_leaderboard_handler(self, make_message):
        """Test leaderboard handler."""
        message = make_message(text="🏆 Рейтинг")
        message.answer = AsyncMock()
        
        await leaderboard_handler(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        assert "Топ игроков" in call_args[0][0]
        assert "reply_markup" in call_args[1]

    @pytest.mark.asyncio
    async def test_help_menu_handler(self, make_message):
        """Test help menu handler."""
        message = make_message(text="ℹ️ Помощь")
        message.answer = AsyncMock()
        
        await help_menu_handler(message)
        
        message.answer.assert_called_once()
        call_args = message.answer.call_args
        
        assert "Помощь и инструкции" in call_args[0][0]
        assert "@ibn_petr" in call_args[0][0]
        assert call_args[1]["parse_mode"] == "HTML"


class TestCallbackHandlers:
    """Test callback query handlers."""

    @pytest.mark.asyncio
    async def test_main_menu_callback(self, make_callback_query):
        """Test main menu callback handler."""
        callback = make_callback_query(data="main_menu")
        callback.message.edit_text = AsyncMock()
        callback.answer = AsyncMock()
        
        await main_menu_callback(callback)
        
        callback.message.edit_text.assert_called_once()
        call_args = callback.message.edit_text.call_args
        
        assert "Главное меню" in call_args[0][0]
        assert call_args[1]["parse_mode"] == "HTML"
        callback.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_quest_callback(self, make_callback_query):
        """Test start quest callback handler."""
        callback = make_callback_query(data="start_quest")
        callback.message.edit_text = AsyncMock()
        callback.answer = AsyncMock()
        
        await start_quest_callback(callback)
        
        callback.message.edit_text.assert_called_once()
        call_args = callback.message.edit_text.call_args
        
        assert "Начинаем квест" in call_args[0][0]
        assert "reply_markup" in call_args[1]
        callback.answer.assert_called_once_with("Скоро добавим квесты! 🚧")