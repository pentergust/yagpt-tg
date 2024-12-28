"""Работа с базой данных пользователей.

Предоставляет модели для хранение пользователя.
"""

from sqlalchemy import BigInteger, Column, DateTime, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from yagpttg.config import config

Base = declarative_base()


class User(Base):
    """Пользователь бота.

    - id: Уникальный идентификатор пользователя.
    - first_name: Имя пользователя.
    - last_name: Фамилия пользователя, может быть не указано.
    - reg_date: Когда пользователь зарегистрировался в боте.
    """

    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    reg_date = Column(DateTime, nullable=False)


engine = create_async_engine(config.db_dsn, echo=True)
SessionLocal = async_sessionmaker(autocommit=False,
                                  autoflush=False,
                                  bind=engine)

