"""Обработчик приветствия.

Отвечает за первое обращения пользователя к боту.
Предлагает пройти простую регистрацию и принять политику конфиденциальности
и условия использования.

После успешное регистрации заносит данные пользователя в базу данных.
"""

from aiogram import Router

router = Router(name="Greeting")

# TODO: Действия при первом запуске бота пользователем
