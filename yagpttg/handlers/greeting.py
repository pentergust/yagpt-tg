"""Обработчик приветствия.

Отвечает за первое обращения пользователя к боту.
Предлагает пройти простую регистрацию и принять политику конфиденциальности
и условия использования.

После успешное регистрации заносит данные пользователя в базу данных.
"""

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from yagpttg import keyboards, messages
from yagpttg.db import User

router = Router(name="Greeting")

# TODO: Действия при первом запуске бота пользователем

@router.message(CommandStart())
async def cmd_start(message: Message, user: User | None) -> None:
    """Приветствуем нового пользователя."""
    if user is None:
        await message.answer(messages.GREETING, reply_markup=keyboards.GREETING)
    else:
        await message.answer(messages.START_WORK)

@router.callback_query(F.data=="reg")
async def register_user_call(query: CallbackQuery, user: User | None) -> None:
    """Регистрирует нового пользователя."""
    if user is not None:
        return await query.answer("🍓 Вы уже проходили регистрацию.")

    user = await User.create(
        id=query.message.from_user.id,
        first_name=query.message.from_user.first_name,
        last_name=query.message.from_user.first_name
    )

    await query.message.answer(messages.START_WORK)
    await query.answer("🍓 Регистрация прошла успешно.")

