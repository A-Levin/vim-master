"""Quest handlers for VimMaster bot."""

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from app.core.services.game import game_service
from app.core.services.quest import quest_service
from app.core.services.user import user_service
from app.db.base import SessionLocal

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("quest"))
async def quest_handler(message: Message) -> None:
    """Handle /quest command - show available quests."""
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

        # Get next recommended quest
        next_quest = game_service.get_next_recommended_quest(db, user.id)

        if not next_quest:
            await message.answer("🎉 Поздравляем! Вы завершили все доступные квесты!")
            return

        # Show quest info
        quest_text = f"""🎯 <b>Квест: {next_quest.title}</b>

<b>Описание:</b>
{next_quest.description}

<b>Тип:</b> {next_quest.quest_type.value.title()}
<b>Сложность:</b> {next_quest.difficulty.value.title()}
<b>Максимум очков:</b> {next_quest.max_score}
{f"<b>Время на выполнение:</b> {next_quest.time_limit} сек" if next_quest.time_limit else ""}

<b>Начальный текст:</b>
<code>{next_quest.initial_text or 'Не указан'}</code>

<b>Ожидаемый результат:</b>
<code>{next_quest.expected_result or 'Выполните команду'}</code>

Готовы начать? Нажмите кнопку ниже!"""

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎮 Начать квест",
                        callback_data=f"start_quest:{next_quest.id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="💡 Получить подсказку",
                        callback_data=f"hint:{next_quest.id}:0",
                    )
                ],
            ]
        )

        await message.answer(quest_text, parse_mode="HTML", reply_markup=keyboard)
    finally:
        db.close()


@router.callback_query(F.data.startswith("start_quest:"))
async def start_quest_callback(callback: CallbackQuery) -> None:
    """Handle start quest callback."""
    if not callback.data or not callback.from_user:
        return

    quest_id = int(callback.data.split(":")[1])

    db = SessionLocal()
    try:
        user = user_service.get_user_by_telegram_id(db, callback.from_user.id)
        if not user:
            await callback.answer("Пользователь не найден.")
            return

        quest = game_service.start_quest(db, user, quest_id)
        if not quest:
            await callback.answer("Квест не найден.")
            return

        await callback.answer("Квест начат! Введите вашу Vim команду.")

        # Set up quest state (in real app, you'd use FSM)
        start_text = f"""🎮 <b>Квест начат: {quest.title}</b>

Введите Vim команду для выполнения задания.

<b>Начальный текст:</b>
<code>{quest.initial_text or ''}</code>

<b>Цель:</b>
<code>{quest.expected_result or 'Выполните команду'}</code>

<i>Введите команду в следующем сообщении...</i>"""

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💡 Подсказка", callback_data=f"hint:{quest.id}:0"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Отменить", callback_data=f"cancel_quest:{quest.id}"
                    )
                ],
            ]
        )

        if callback.message:
            await callback.message.edit_text(
                start_text, parse_mode="HTML", reply_markup=keyboard
            )

    finally:
        db.close()


@router.callback_query(F.data.startswith("hint:"))
async def hint_callback(callback: CallbackQuery) -> None:
    """Handle hint request callback."""
    if not callback.data or not callback.from_user:
        return

    parts = callback.data.split(":")
    quest_id = int(parts[1])
    hints_used = int(parts[2])

    db = SessionLocal()
    try:
        quest = quest_service.get_quest_by_id(db, quest_id)
        if not quest:
            await callback.answer("Квест не найден.")
            return

        hint = game_service.get_quest_hints(quest, hints_used)
        if not hint:
            await callback.answer("Больше подсказок нет!")
            return

        hint_text = f"💡 <b>Подсказка {hints_used + 1}:</b>\n{hint}"

        # Update keyboard with next hint button
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💡 Еще подсказка",
                        callback_data=f"hint:{quest_id}:{hints_used + 1}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Отменить", callback_data=f"cancel_quest:{quest_id}"
                    )
                ],
            ]
        )

        await callback.answer()
        await callback.message.answer(hint_text, parse_mode="HTML")

    finally:
        db.close()


@router.message(
    F.text.startswith(":") | F.text.startswith(".") | F.text.startswith("g")
)
async def quest_answer_handler(message: Message) -> None:
    """Handle potential quest answer (Vim command)."""
    telegram_user = message.from_user
    if not telegram_user or not message.text:
        return

    db = SessionLocal()
    try:
        user = user_service.get_user_by_telegram_id(db, telegram_user.id)
        if not user:
            return

        # Get the next recommended quest (simplified - in real app use FSM)
        next_quest = game_service.get_next_recommended_quest(db, user.id)
        if not next_quest:
            return

        # Submit answer
        is_correct, score, result_message = game_service.submit_answer(
            db, user, next_quest.id, message.text
        )

        if is_correct:
            success_text = f"""✅ <b>Правильно!</b>

{result_message}

<b>Команда:</b> <code>{message.text}</code>
<b>Получено очков:</b> {score}

🎉 Квест "{next_quest.title}" завершен!"""

            # Show next quest button
            next_quest_after = game_service.get_next_recommended_quest(db, user.id)
            if next_quest_after:
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="➡️ Следующий квест",
                                callback_data=f"start_quest:{next_quest_after.id}",
                            )
                        ]
                    ]
                )
                await message.answer(
                    success_text, parse_mode="HTML", reply_markup=keyboard
                )
            else:
                await message.answer(
                    success_text + "\n\n🏆 Вы завершили все доступные квесты!",
                    parse_mode="HTML",
                )
        else:
            failure_text = f"""❌ <b>Неправильно</b>

{result_message}

<b>Ваша команда:</b> <code>{message.text}</code>

Попробуйте еще раз или используйте подсказку."""

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="💡 Подсказка", callback_data=f"hint:{next_quest.id}:0"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🔄 Попробовать снова",
                            callback_data=f"start_quest:{next_quest.id}",
                        )
                    ],
                ]
            )

            await message.answer(failure_text, parse_mode="HTML", reply_markup=keyboard)

    finally:
        db.close()


@router.callback_query(F.data.startswith("cancel_quest:"))
async def cancel_quest_callback(callback: CallbackQuery) -> None:
    """Handle quest cancellation."""
    await callback.answer("Квест отменен.")
    if callback.message:
        await callback.message.edit_text(
            "Квест отменен. Используйте /quest для выбора нового квеста."
        )
