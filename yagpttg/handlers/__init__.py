"""Подгрузка всех роутеров.

Весь функционал бота был поделён на различные обработчики для
большей гибкости.
"""

from yagpttg.handlers import gpt, greeting

ROUTERS = (
    greeting.router,

    # Загружается последним, поскольку перехватывает все сообщения
    gpt.router
)

__all__ = ("ROUTERS",)
