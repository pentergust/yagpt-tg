"""Обращение к YandexGPI API.

Предоставляет класс для общения с API от имени пользователя.
"""

import requests


class YandexGPTAPI:
    """Позволяет пользователю обращаться к YandexGPT API."""

    def __init__(self) -> None:
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "AQVNy9EyL2PskKxswPfKr9j87g-QDMY2NjT8bcmq"
        }

        self.prompt = {
            "modelUri": "gpt://ajebq4p2uovci2m6pg7n/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 2000
            },
            "messages": []
        }
        self.response = requests.post(
            self.url, headers=self.headers, json=self.prompt
        )
        self.result = self.response.text

    def get_answer(self, text: str) -> dict | None:
        """Получает ответ на запрос к API."""
        self.prompt['messages'].append({"role": 'user', "text": text})
        try:
            response = requests.post(
                url=self.url, headers=self.headers, json=self.prompt
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к YandexGPT API: {e}")

yandex_gpt_api = YandexGPTAPI()
