"""Обработчик GPT.

Позволяет пользователю общаться с YandexGPT.
"""


from asyncio import sleep

from aiogram import Bot, Router
from aiogram.enums import ChatAction
from aiogram.types import Message

from yagpttg.db import User

# from yagpttg.api import yandex_gpt_api

router = Router(name="YandexGPT")

# TODO: Тут мы общаемся с YandexGPT

@router.message()
async def send_user_gpt_answer(
    message: Message,
    user: User | None,
    bot: Bot
) -> None:
    """Получаем сообщения юзера и отправляем запрос в YandexGpt.

    После отправляем ответ обратно пользователю.
    """
    if user is None:
        if message.chat.type == "private":
            await message.answer(text=(
                "🍓 Перед тем как вы начнёте пользоваться ботом, "
                "стоит пройти регистрацию."
            ))
        return None

    if message.text is None:
        if message.chat.type == "private":
            await message.answer(
                "Пожалуйста, отправьте мне текст сообщения."
            )
        return None

    prompt = message.text.strip()

    answer = await message.answer("⏳ Ответ подготавливается...")
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    # TODO: Вместо sleep() тут разумеется обработка сообщения
    await sleep(3)

    await answer.edit_text(prompt)

