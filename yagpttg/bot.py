"""Главный файл бота.

Здесь определены функции для запуска бота и регистрации всех обработчиков.
"""

import sys

from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent
from aiogram.utils.token import TokenValidationError
from loguru import logger
from tortoise import Tortoise

from yagpttg.config import config, default
from yagpttg.handlers import ROUTERS

# Константы
# =========

dp = Dispatcher()

# Настраиваем формат отображения логов loguru
# Обратите внимание что в проекте помимо loguru используется logging
LOG_FORMAT = (
    "<light-black>{time:YYYY MM.DD HH:mm:ss.SSS}</> "
    "{file}:{function} "
    "<lvl>{message}</>"
)

# Middleware
# ==========

@dp.errors()
async def catch_errors(event: ErrorEvent) -> None:
    """Простой обработчик для ошибок."""
    logger.warning(event)
    logger.exception(event.exception)


# Главная функция запуска бота
# ============================

async def main() -> None:
    """Запускает бота.

    Настраивает loguru.
    Загружает все необходимые обработчики.
    После запускает Long polling.
    """
    logger.remove()
    logger.add(sys.stdout, format=LOG_FORMAT)

    logger.info("Check config")
    logger.debug("Token: {}", config.bot_token)
    logger.debug("DB: {}", config.db_dsn)
    logger.debug("Cache: {}", config.redis_dsn)

    logger.info("Setup bot ...")
    try:
        bot = Bot(
            token=config.bot_token.get_secret_value(),
            default=default
        )
    except TokenValidationError as e:
        logger.error(e)
        logger.info("Check your bot token in .env file.")
        sys.exit(1)

    logger.info("Load handlers ...")
    for router in ROUTERS:
        dp.include_router(router)
        logger.debug("Include router {}", router.name)

    logger.info("Init db connection ...")
    await Tortoise.init(
        db_url=str(config.db_dsn),
        modules={"models": ["yagpttg.db"]}
    )
    await Tortoise.generate_schemas()

    logger.success("Start polling!")
    await dp.start_polling(bot)
