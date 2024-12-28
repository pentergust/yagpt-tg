"""Обращение к YandexGPI API.

Предоставляет класс для общения с API от имени пользователя.
"""

import aiohttp
from loguru import logger

from yagpttg.cache import RedisCacheStorage


class YandexGPT:
    """Позволяет пользователю обращаться к YandexGPT API."""

    def __init__(self, folder_id: str, iam_token: str) -> None:
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {iam_token}"
        }

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

        # Дополняем переписку контекстом ранее
        if await self.rd_bd.have_user(key=user_id) == 1:
            messages = await self.rd_bd.bd(key=user_id)
            request["messages"].extend(messages)
            request["messages"].append({"role": "user", "text": f"{prompt}"})

        # Выполняем запрос к GPT
        try:
            response = await self._session.post(
                url=self.url,
                headers=self.headers,
                json=request
            )
            json_resp = await response.json()
            await self.rd_bd.bd(key=user_id, prompt=prompt, answer=json_resp)
            return response['result']['alternatives'][0]['message']
        except Exception as e:
            logger.error("Ошибка при запросе к YandexGPT API: {}", e)
