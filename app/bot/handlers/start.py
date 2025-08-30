"""Start command handler for VimMaster bot."""

import logging
from typing import Any

from aiogram import Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.keyboards.main import get_main_keyboard
from app.core.services.game import game_service
from app.core.services.user import user_service
from app.db.base import SessionLocal

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, **kwargs: Any) -> None:
    """
    Handle /start command.

    This handler is called when user first starts the bot or sends /start.
    It shows welcome message and main menu.
    """
    telegram_user = message.from_user
    if not telegram_user:
        return

    logger.info(f"User {telegram_user.id} ({telegram_user.username}) started the bot")

    # Create or get user from database
    db = SessionLocal()
    try:
        user = user_service.get_or_create_user(
            db,
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
        )

        welcome_text = f"""🎮 <b>Добро пожаловать в VimMaster!</b>

Привет, {html.bold(telegram_user.first_name)}! 👋

VimMaster — это интерактивная игра для изучения Vim через практические квесты.

<b>Что тебя ждет:</b>
• 📚 Изучение команд Vim от базовых до продвинутых
• 🎯 Практические квесты и задания
• 🏆 Система очков и достижений
• 📈 Отслеживание прогресса

<b>Твой текущий уровень:</b> {user_service.calculate_level(user.total_score)}
<b>Очки:</b> {user.total_score}

<b>Начни свое путешествие в мир Vim прямо сейчас!</b>

Выбери действие в меню ниже:"""

        await message.answer(
            welcome_text,
            reply_markup=get_main_keyboard(),
            parse_mode="HTML",
        )
    finally:
        db.close()


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
    telegram_user = message.from_user
    if not telegram_user:
        return

    db = SessionLocal()
    try:
        user = user_service.get_user_by_telegram_id(db, telegram_user.id)
        if not user:
            await message.answer(
                "Пользователь не найден. Используйте /start для регистрации."
            )
            return

        # Get user progress summary
        progress_summary = game_service.get_user_progress_summary(db, user.id)
        current_level = user_service.calculate_level(user.total_score)

        profile_text = f"""👤 <b>Профиль игрока</b>

<b>Имя:</b> {html.bold(telegram_user.first_name or "Не указано")}
<b>Username:</b> @{telegram_user.username or "не установлен"}
<b>ID:</b> <code>{telegram_user.id}</code>

📊 <b>Статистика:</b>
• Уровень: {current_level}
• Очки: {user.total_score}
• Квестов завершено: {progress_summary['total_completed']}
• Попыток всего: {progress_summary['total_attempts']}
• Процент успеха: {progress_summary['completion_rate'] * 100:.1f}%

🏆 <b>Достижения:</b>
{"Пока нет достижений" if progress_summary['total_completed'] == 0 else f"Завершено квестов: {progress_summary['total_completed']}"}

<i>Продолжайте проходить квесты, чтобы улучшить статистику!</i>"""

        await message.answer(profile_text, parse_mode="HTML")
    finally:
        db.close()
