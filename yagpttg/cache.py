"""Кеширование запросов к API."""

import json

from redis.asyncio import Redis

from yagpttg.Yandextoken import IamTokem

# Константы
# =========

# время кеширования данных в Redis (в секундах)
_CACHE_TIME = 3600

class RedisCacheStorage:
    """Кеширование запросов к API.

    Позволяет кешировать запросы к API и хранить контекст общения.
    """

    def __init__(self, client: Redis | None = None, ttl: int = None) -> None:
        """Создаёт новое подключение к Redis для кеша.

        По умолчанию создаёт новое подключение к локальной базе данных.
        Вы можете передать сюда любое другое подключение к Redis.

        Args:
            client (Redis | None): Клиент для использования.
            ttl (int, optional): Время хранения данных в Redis (в секундах).
        """
        self.client = client or Redis()
        self.ttl = ttl if isinstance(ttl, int) else _CACHE_TIME
        self.tokens = IamTokem()

    async def bd(self,
        key: str,
        prompt: str | None = None,
        answer: dict | None = None
    ) -> str | None:
        """Кеширует промпт пользователя и ответ к нему."""
        exs = await self.client.exists(key)

        if prompt is None or answer is None:
            if exs == 1:
                return json.loads(await self.client.get(key))
            return None

        ans = answer['result']['alternatives'][0]['message']
        if exs == 0:
            await self.client.set(
                key,
                json.dumps([prompt, ans]),
                ex=self.ttl
            )
            return "Complete"

        data = json.loads(await self.client.get(key))
        data.append(prompt)
        data.append(ans)
        await self.client.set(key, json.dumps(data), ex = self.ttl)
        return "Complete"

    async def have_user(self, user: str) -> bool:
        """Проверяет что пользователь есть в кеш хранилище."""
        return await self.client.exists(user) == 1

    async def imtoken(self) -> str | None:
        if await self.client.exists("imkey") == 0:
            token = await self.tokens.get_token()
            await self.client.set("imkey", token, ex=self.ttl)
        else:
            token = await self.client.get("imkey")
        return token


