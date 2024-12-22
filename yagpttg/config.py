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
    - db_url: Путь для подключения к базе данных.
    """

    bot_token: SecretStr
    db_dsn: PostgresDsn
    redis_dsn: RedisDsn

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
