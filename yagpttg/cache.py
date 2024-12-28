"""Кеширование запросов к API.

"""

import json
import asyncio
import redis.asyncio as redis

# Константы
# =========

# время кеширования данных в Redis (в минутах?)
_CACHE_TIME = 3600

class RedisCacheStorage:
    """Кеширование запросов к API.

    Позволяет кешировать запросы к API и хранить контекст общения.
    """

    def __init__(self, cl = None, time = None) -> None:
        if cl is not None:
            self.client = cl
        else:
            self.client = redis.Redis(host='127.0.0.1')
        if time is not None and isinstance(time, int | float):
            self.time = time
        else:
            self.time = _CACHE_TIME

    async def bd(self, key, question = None, answer = None) -> str | None:
        key = str(key)
        exs = await self.client.exists(key)

        if question is None or answer is None:
            if exs == 1:
                return json.loads(await self.client.get(key))
            return None

        ans = answer['result']['alternatives'][0]['message']
        if exs == 0:
            await self.client.set(key, json.dumps([question, ans]), ex = self.time)
            return "Complete"

        data = json.loads(await self.client.get(key))
        data.append(question)
        data.append(ans)
        await self.client.set(key, json.dumps(data), ex = self.time)
        return "Complete"

