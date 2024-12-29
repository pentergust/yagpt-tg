import time
import jwt
import json
import asyncio
from loguru import logger
import aiohttp

class Iam_Tokem:


    def __init__(self, filename: str | None = None) -> None:
        if filename is None:
            filename = 'yagpttg/key.json'
        with open(filename, 'r') as f: 
            obj = f.read() 
            obj = json.loads(obj)
            self.private_key = obj['private_key']
            self.key_id = obj['id']
            self.service_account_id = obj['service_account_id']
            self._session = aiohttp.ClientSession()

    async def get_token(self):
        now = int(time.time())
        payload = {
                'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                'iss': self.service_account_id,
                'iat': now,
                'exp': now + 3600
            }
        # Формирование JWT.
        encoded_token = jwt.encode(
            payload,
            self.private_key,
            algorithm='PS256',
            headers={'kid': self.key_id}
        )
        #Запись ключа
        logger.debug(encoded_token)
        response = await self._session.post(
            url="https://iam.api.cloud.yandex.net/iam/v1/tokens",
            headers='Content-Type: application/json',
            json={"jwt":f"{encoded_token}"}
        )
        return response.text()

