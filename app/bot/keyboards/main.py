"""Main keyboards for VimMaster bot."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎯 Квесты"),
                KeyboardButton(text="👤 Профиль"),
            ],
            [
                KeyboardButton(text="📚 Обучение"),
                KeyboardButton(text="🏆 Рейтинг"),
            ],
            [
                KeyboardButton(text="ℹ️ Помощь"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие...",
    )
    return keyboard


def get_quest_keyboard() -> InlineKeyboardMarkup:
    """Get quest selection keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 Начать новый квест", callback_data="start_quest"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📊 Мой прогресс", callback_data="quest_progress"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔙 В главное меню", callback_data="main_menu"
                ),
            ],
        ]
    )
    return keyboard


def get_learning_keyboard() -> InlineKeyboardMarkup:
    """Get learning materials keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📖 Основы Vim", callback_data="learn_basics"
                ),
                InlineKeyboardButton(
                    text="⌨️ Команды", callback_data="learn_commands"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎯 Движения", callback_data="learn_motions"
                ),
                InlineKeyboardButton(
                    text="✏️ Редактирование", callback_data="learn_editing"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Поиск", callback_data="learn_search"
                ),
                InlineKeyboardButton(
                    text="🎭 Макросы", callback_data="learn_macros"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔙 В главное меню", callback_data="main_menu"
                ),
            ],
        ]
    )
    return keyboard


def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Get profile management keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Подробная статистика", callback_data="detailed_stats"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏆 Мои достижения", callback_data="my_achievements"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Настройки", callback_data="settings"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔙 В главное меню", callback_data="main_menu"
                ),
            ],
        ]
    )
    return keyboard


def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """Get simple back to main menu keyboard."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 В главное меню", callback_data="main_menu"
                ),
            ],
        ]
    )
    return keyboard