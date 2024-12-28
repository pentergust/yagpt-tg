"""Константные настройки бота.

Данные настройки загружаются один раз при запуске бота и больше не
изменяются по ходу работы бота.
"""

from aiogram.client.default import DefaultBotProperties
from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Общие настройки бота
# ====================

class BotConfig(BaseSettings):
    """Общие настройки бота.

    Загружаются один раз при запуске бота и после не могут быть
    изменены.

    - bot_token: Токен от Telegram бота.
    - db_dsn: Данные для подключения к базе данных.
    - redis_dsn: Данные для подключения к кешу.
    - ya_gpt_key: API ключ для взаимодействия с Yandex GPT.
    """

    bot_token: SecretStr
    db_dsn: PostgresDsn
    redis_dsn: RedisDsn

    folder_id: SecretStr
    yagpt_token: SecretStr

    # Настраиваем подгрузку из .env файла
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

config = BotConfig()

# Настройки telgram бота по умолчанию для Aiogram
default = DefaultBotProperties(
    parse_mode="html"
)
