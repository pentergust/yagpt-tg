"""Работа с базой данных пользователей.

Предоставляет модели для хранение пользователя.

Пока что на Tortoise-ORM, после может быть переписано на алхимию.
"""

from tortoise import Model, fields

class User(Model):
    """Пользователь бота.

    - id: Уникальный идентификатор пользователя.
    - first_name: Имя пользователя.
    - last_name: Фамилия пользователя, может быть не указано.
    - reg_data: Когда пользователь зарегистрировался в боте.
    """

    id = fields.BigIntField(primary_key=True)
    first_name = fields.TextField()
    last_name = fields.TextField()
    reg_date = fields.DatetimeField(auto_now_add=True)
