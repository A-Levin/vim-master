"""Start command handler for VimMaster bot."""

import logging
from typing import Any

from aiogram import Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.keyboards.main import get_main_keyboard

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, **kwargs: Any) -> None:
    """
    Handle /start command.
    
    This handler is called when user first starts the bot or sends /start.
    It shows welcome message and main menu.
    """
    user = message.from_user
    if not user:
        return

    logger.info(f"User {user.id} ({user.username}) started the bot")

    welcome_text = f"""🎮 <b>Добро пожаловать в VimMaster!</b>

Привет, {html.bold(user.first_name)}! 👋

VimMaster — это интерактивная игра для изучения Vim через практические квесты. 

<b>Что тебя ждет:</b>
• 📚 Изучение команд Vim от базовых до продвинутых
• 🎯 Практические квесты и задания
• 🏆 Система очков и достижений
• 📈 Отслеживание прогресса

<b>Начни свое путешествие в мир Vim прямо сейчас!</b>

Выбери действие в меню ниже:"""

    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Handle /help command."""
    help_text = """📖 <b>Помощь по VimMaster</b>

<b>Основные команды:</b>
/start - Начать или перезапустить бота
/profile - Посмотреть свой профиль
/quest - Начать новый квест
/help - Показать эту справку

<b>Как играть:</b>
1. Начните с простых квестов в разделе "🎯 Квесты"
2. Выполняйте задания, вводя Vim команды
3. Получайте очки за правильные ответы
4. Открывайте новые уровни и достижения

<b>Нужна помощь?</b>
• Используйте подсказки в квестах
• Обратитесь к справке Vim: :help команда
• Изучайте материалы в разделе "📚 Обучение"

<b>Удачи в изучении Vim! 🚀</b>"""

    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("profile"))
async def profile_handler(message: Message) -> None:
    """Handle /profile command."""
    user = message.from_user
    if not user:
        return

    # TODO: Get user data from database
    profile_text = f"""👤 <b>Профиль игрока</b>

<b>Имя:</b> {html.bold(user.first_name or "Не указано")}
<b>Username:</b> @{user.username or "не установлен"}
<b>ID:</b> <code>{user.id}</code>

📊 <b>Статистика:</b>
• Уровень: 1
• Очки: 0
• Квестов завершено: 0
• Дней подряд: 0

🏆 <b>Достижения:</b>
Пока нет достижений

<i>Начните проходить квесты, чтобы улучшить статистику!</i>"""

    await message.answer(profile_text, parse_mode="HTML")