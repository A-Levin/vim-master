"""Tests for bot keyboards."""

import pytest
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from app.bot.keyboards.main import (
    get_main_keyboard,
    get_quest_keyboard,
    get_learning_keyboard,
    get_profile_keyboard,
    get_back_to_main_keyboard,
)


class TestMainKeyboards:
    """Test main keyboard functions."""

    def test_get_main_keyboard(self):
        """Test main keyboard creation."""
        keyboard = get_main_keyboard()
        
        assert isinstance(keyboard, ReplyKeyboardMarkup)
        assert keyboard.resize_keyboard is True
        assert keyboard.one_time_keyboard is False
        assert "Выберите действие..." in keyboard.input_field_placeholder
        
        # Check keyboard structure
        assert len(keyboard.keyboard) == 3  # 3 rows
        assert len(keyboard.keyboard[0]) == 2  # First row: 2 buttons
        assert len(keyboard.keyboard[1]) == 2  # Second row: 2 buttons
        assert len(keyboard.keyboard[2]) == 1  # Third row: 1 button
        
        # Check button texts
        first_row_texts = [btn.text for btn in keyboard.keyboard[0]]
        assert "🎯 Квесты" in first_row_texts
        assert "👤 Профиль" in first_row_texts
        
        second_row_texts = [btn.text for btn in keyboard.keyboard[1]]
        assert "📚 Обучение" in second_row_texts
        assert "🏆 Рейтинг" in second_row_texts
        
        third_row_texts = [btn.text for btn in keyboard.keyboard[2]]
        assert "ℹ️ Помощь" in third_row_texts

    def test_get_quest_keyboard(self):
        """Test quest keyboard creation."""
        keyboard = get_quest_keyboard()
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 3  # 3 rows
        
        # Check callback data
        callback_data = [
            btn.callback_data 
            for row in keyboard.inline_keyboard 
            for btn in row
        ]
        assert "start_quest" in callback_data
        assert "quest_progress" in callback_data
        assert "main_menu" in callback_data
        
        # Check button texts
        button_texts = [
            btn.text 
            for row in keyboard.inline_keyboard 
            for btn in row
        ]
        assert "🎮 Начать новый квест" in button_texts
        assert "📊 Мой прогресс" in button_texts
        assert "🔙 В главное меню" in button_texts

    def test_get_learning_keyboard(self):
        """Test learning keyboard creation."""
        keyboard = get_learning_keyboard()
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 4  # 4 rows
        
        # Check first row has 2 buttons
        assert len(keyboard.inline_keyboard[0]) == 2
        
        # Check callback data exists
        callback_data = [
            btn.callback_data 
            for row in keyboard.inline_keyboard 
            for btn in row
        ]
        expected_callbacks = [
            "learn_basics", "learn_commands", "learn_motions",
            "learn_editing", "learn_search", "learn_macros", "main_menu"
        ]
        for callback in expected_callbacks:
            assert callback in callback_data
        
        # Check button texts
        button_texts = [
            btn.text 
            for row in keyboard.inline_keyboard 
            for btn in row
        ]
        assert "📖 Основы Vim" in button_texts
        assert "⌨️ Команды" in button_texts
        assert "🎭 Макросы" in button_texts

    def test_get_profile_keyboard(self):
        """Test profile keyboard creation."""
        keyboard = get_profile_keyboard()
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 4  # 4 rows
        
        # Check callback data
        callback_data = [
            btn.callback_data 
            for row in keyboard.inline_keyboard 
            for btn in row
        ]
        expected_callbacks = [
            "detailed_stats", "my_achievements", "settings", "main_menu"
        ]
        for callback in expected_callbacks:
            assert callback in callback_data
        
        # Check button texts
        button_texts = [
            btn.text 
            for row in keyboard.inline_keyboard 
            for btn in row
        ]
        assert "📊 Подробная статистика" in button_texts
        assert "🏆 Мои достижения" in button_texts
        assert "⚙️ Настройки" in button_texts

    def test_get_back_to_main_keyboard(self):
        """Test back to main keyboard creation."""
        keyboard = get_back_to_main_keyboard()
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 1  # 1 row
        assert len(keyboard.inline_keyboard[0]) == 1  # 1 button
        
        button = keyboard.inline_keyboard[0][0]
        assert button.text == "🔙 В главное меню"
        assert button.callback_data == "main_menu"

    def test_keyboards_are_not_none(self):
        """Test that all keyboard functions return valid objects."""
        keyboards = [
            get_main_keyboard(),
            get_quest_keyboard(),
            get_learning_keyboard(),
            get_profile_keyboard(),
            get_back_to_main_keyboard(),
        ]
        
        for keyboard in keyboards:
            assert keyboard is not None
            assert hasattr(keyboard, 'keyboard') or hasattr(keyboard, 'inline_keyboard')

    def test_keyboard_button_structure(self):
        """Test keyboard button structure consistency."""
        inline_keyboards = [
            get_quest_keyboard(),
            get_learning_keyboard(),
            get_profile_keyboard(),
            get_back_to_main_keyboard(),
        ]
        
        for keyboard in inline_keyboards:
            for row in keyboard.inline_keyboard:
                for button in row:
                    # Each button should have text and callback_data
                    assert hasattr(button, 'text')
                    assert hasattr(button, 'callback_data')
                    assert button.text is not None
                    assert button.callback_data is not None
                    assert len(button.text) > 0
                    assert len(button.callback_data) > 0