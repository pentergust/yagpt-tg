"""Обработчик GPT.

Позволяет пользователю общаться с YandexGPT.
"""

from aiogram import Bot, Router
from aiogram.enums import ChatAction
from aiogram.types import Message
from loguru import logger

from yagpttg.api import YandexGPT
from yagpttg.db import User

router = Router(name="YandexGPT")


# Обработчики
# ===========

@router.message()
async def send_user_gpt_answer(
    message: Message,
    user: User | None,
    bot: Bot,
    yagpt: YandexGPT
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

    answer = await message.answer("⏳ Думаю...")
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    try:
        resp = await yagpt.get_answer(str(message.from_user.id), prompt)
    except Exception as e:
        logger.error("Error while processing GPT request: {}", e)
        await answer.edit_text("🔌 Во время работы произошла некоторая ошибка.")
    else:
        await answer.edit_text(resp)

