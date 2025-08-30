"""Menu navigation handlers for VimMaster bot."""

import logging
from typing import Any

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.main import (
    get_back_to_main_keyboard,
    get_learning_keyboard,
    get_profile_keyboard,
    get_quest_keyboard,
)

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "🎯 Квесты")
async def quests_menu_handler(message: Message, **kwargs: Any) -> None:
    """Handle quests menu."""
    quests_text = """🎯 <b>Квесты и задания</b>

Добро пожаловать в раздел квестов! Здесь ты можешь:

• <b>Проходить интерактивные задания</b> по Vim
• <b>Изучать команды</b> на практике
• <b>Получать очки</b> за правильные ответы
• <b>Отслеживать прогресс</b>

<i>Квесты разделены на уровни сложности от новичка до эксперта.</i>

Выбери действие:"""

    await message.answer(
        quests_text,
        reply_markup=get_quest_keyboard(),
        parse_mode="HTML",
    )


@router.message(F.text == "📚 Обучение")
async def learning_menu_handler(message: Message, **kwargs: Any) -> None:
    """Handle learning menu."""
    learning_text = """📚 <b>Материалы для обучения</b>

Изучай Vim систематически:

• <b>Основы Vim</b> — режимы работы, философия
• <b>Команды</b> — основные и продвинутые
• <b>Движения</b> — навигация по тексту
• <b>Редактирование</b> — изменение текста
• <b>Поиск</b> — поиск и замена
• <b>Макросы</b> — автоматизация действий

<i>Каждый раздел содержит теорию и практические примеры.</i>"""

    await message.answer(
        learning_text,
        reply_markup=get_learning_keyboard(),
        parse_mode="HTML",
    )


@router.message(F.text == "👤 Профиль")
async def profile_menu_handler(message: Message, **kwargs: Any) -> None:
    """Handle profile menu."""
    user = message.from_user
    if not user:
        return

    # TODO: Get actual user data from database
    profile_text = f"""👤 <b>Профиль игрока</b>

<b>Основная информация:</b>
• Имя: {user.first_name or "Не указано"}
• Username: @{user.username or "не установлен"}

📊 <b>Игровая статистика:</b>
• Уровень: 1 🌟
• Общие очки: 0
• Квестов завершено: 0 / 50
• Дней активности подряд: 0 🔥

🏆 <b>Последние достижения:</b>
<i>Пока нет достижений</i>

💡 <i>Совет: Начни с базовых квестов, чтобы получить первые очки!</i>"""

    await message.answer(
        profile_text,
        reply_markup=get_profile_keyboard(),
        parse_mode="HTML",
    )


@router.message(F.text == "🏆 Рейтинг")
async def leaderboard_handler(message: Message, **kwargs: Any) -> None:
    """Handle leaderboard."""
    # TODO: Get actual leaderboard data
    leaderboard_text = """🏆 <b>Топ игроков</b>

<b>🥇 ТОП-10 по очкам:</b>
<i>Пока нет данных</i>

<b>🔥 Самые активные:</b>
<i>Пока нет данных</i>

<b>⚡ Быстрые решения:</b>
<i>Пока нет данных</i>

<i>Начни проходить квесты, чтобы попасть в рейтинг!</i>"""

    await message.answer(
        leaderboard_text,
        reply_markup=get_back_to_main_keyboard(),
        parse_mode="HTML",
    )


@router.message(F.text == "ℹ️ Помощь")
async def help_menu_handler(message: Message, **kwargs: Any) -> None:
    """Handle help menu."""
    help_text = """ℹ️ <b>Помощь и инструкции</b>

<b>🎮 Как играть:</b>
1. Выбери квест в разделе "🎯 Квесты"
2. Читай задание внимательно
3. Вводи Vim команды в ответ
4. Получай очки за правильные ответы

<b>💡 Полезные советы:</b>
• Начинай с базовых квестов
• Используй подсказки, если застрял
• Изучай материалы в разделе "📚 Обучение"
• Практикуйся каждый день

<b>📝 Синтаксис ввода:</b>
• Вводи команды как в настоящем Vim
• Например: <code>dd</code>, <code>yy</code>, <code>:w</code>
• Не добавляй лишних символов

<b>🆘 Нужна помощь?</b>
Пиши @ibn_petr — разработчику бота

<b>Удачного изучения Vim! 🚀</b>"""

    await message.answer(
        help_text,
        reply_markup=get_back_to_main_keyboard(),
        parse_mode="HTML",
    )


# Callback handlers for inline keyboards
@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery) -> None:
    """Handle main menu callback."""
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\nВыберите действие:",
        reply_markup=None,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "start_quest")
async def start_quest_callback(callback: CallbackQuery) -> None:
    """Handle start quest callback."""
    # TODO: Implement quest starting logic
    await callback.message.edit_text(
        "🎮 <b>Начинаем квест!</b>\n\n<i>Функция скоро будет доступна...</i>",
        reply_markup=get_back_to_main_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer("Скоро добавим квесты! 🚧")
