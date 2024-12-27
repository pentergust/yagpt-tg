"""Обработчик приветствия.

Отвечает за первое обращения пользователя к боту.
Предлагает пройти простую регистрацию и принять политику конфиденциальности
и условия использования.

После успешное регистрации заносит данные пользователя в базу данных.
"""

from aiogram import Router, types
from aiogram.filters import CommandStart

from yagpttg import keyboards, messages

router = Router(name="Greeting")

# TODO: Действия при первом запуске бота пользователем


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    """Приветствуем нового пользователя."""
    await message.answer(messages.GREETING, reply_markup=keyboards.GREETING)

