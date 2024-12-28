"""Обращение к YandexGPI API.

Предоставляет класс для общения с API от имени пользователя.

"""
import asyncio
import aiohttp
import cache


class YandexGPTAPI:
    """Позволяет пользователю обращаться к YandexGPT API."""

    def __init__(self, folder_id, iam_token) -> None:
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {iam_token}"
        }

        self.prompt = {
            "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 2000
            },
            "messages": []
        }
        
        self.rd_bd = cache.RedisCacheStorage()

    async def get_answer(self, tg_id, text: str) -> dict | None:
        """Получает ответ на запрос к API."""
        prom = self.prompt
        if await self.rd_bd.have_user(key = tg_id) == 1:
                data = await self.rd_bd.bd(key = tg_id)
                prom["messages"].extend(data)
                prom["messages"].append({"role": "user", "text": f"{text}"})
        
        try:
            #session = aiohttp.ClientSession(raise_for_status=True)
            async with aiohttp.ClientSession() as session:
                response = await session.post(url=self.url, headers=self.headers, json=prom)
                resp = await response.json()
                await self.rd_bd(key = tg_id, question = text, answer = resp)
                return response['result']['alternatives'][0]['message']
        except Exception as e:
            print(f"Ошибка при запросе к YandexGPT API: {e}")

yandex_gpt_api = YandexGPTAPI("fdfdfd", "dsds")
asyncio.run(yandex_gpt_api.get_answer(42343, "Привет"))
