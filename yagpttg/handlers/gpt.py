"""Обработчик GPT.

Позволяет пользователю общаться с YandexGPT.
"""

from aiogram import Router, types

from yagpttg.api import yandex_gpt_api

router = Router(name="YandexGPT")

# TODO: Тут мы общаемся с YandexGPT

@router.message()
async def send_user_gpt_answer(message: types.Message) -> None:
    """Получаем сообщения юзера и отправляем запрос в YandexGpt.

    После Отправляем ответ обратно пользователю.
    """
    gpt_response = yandex_gpt_api.get_answer(role='user', text=message.text)

    if gpt_response:
        gpt_message = gpt_response.get(
            'choices', [{}]
        )[0].get('text', 'Нет ответа')
        print(gpt_message)
