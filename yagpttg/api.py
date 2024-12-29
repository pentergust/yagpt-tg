"""Обращение к YandexGPI API.

Предоставляет класс для общения с API от имени пользователя.
"""

import aiohttp
from loguru import logger

from yagpttg.cache import RedisCacheStorage


class YandexAPIError(Exception):
    """Если что-то во время работы с GPT пошло не по плану."""

class YandexGPT:
    """Позволяет пользователю обращаться к YandexGPT API."""

    def __init__(self, folder_id: str) -> None:
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.request_prompt = {
            "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 2000
            },
            "messages": []
        }

        self.rd_bd = RedisCacheStorage()
        self._session = aiohttp.ClientSession()

    async def get_answer(self, user_id: str, prompt: str) -> dict | None:
        """Получает ответ на запрос к API."""
        request = self.request_prompt.copy()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {await self.rd_bd.iamtoken()}"
        }
        # Дополняем переписку контекстом ранее
        if await self.rd_bd.have_user(user=user_id) == 1:
            messages = await self.rd_bd.bd(key=user_id)
            request["messages"].extend(messages)
            request["messages"].append({"role": "user", "text": f"{prompt}"})

        # Выполняем запрос к GPT
        response = await self._session.post(
            url=self.url,
            headers=headers,
            json=request
        )
        json_resp = await response.json()
        logger.debug(json_resp)
        if "error" in json_resp:
            raise YandexAPIError(json_resp)

        await self.rd_bd.bd(key=user_id, prompt=prompt, answer=json_resp)
        return json_resp['result']['alternatives'][0]['message']
