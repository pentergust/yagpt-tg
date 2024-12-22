"""Подгрузка всех роутеров.

Весь функционал бота был поделён на различные обработчики для
большей гибкости.
"""

from yagpttg.handlers import gpt, greeting

ROUTERS = (
    gpt.router,
    greeting.router
)

__all__ = ("ROUTERS",)
