# YaGPT (tg)

Бот позволяет вам общаться с **YandexGPT** в ваших Telegram чатах!

## Установка

Для того чтобы запустить бота локально, вам потребуется:

- [poetry](https://python-poetry.org).
- PostgreSQL.
- Telegram бот.
- Redis.

Первым делом клонируем репозиторий проекта:

```sh
git clone https://github.com/pentergust/yagpt-tg
```

Теперь установим все зависимости для проекта через *Poetry*:

```sh
poetry install
```

После, до первого запуска нужно настроить бота, для этого нужно скопировать
файл `.env.dist` в `.env` и изменить настройки под себя.

Вот и всё, можно запускать бота:

```sh
poetry run python -m yagpttg
```

Как видно, ничего сложного в установке нету :)

## Авторы

- [@pentergust](https://www.github.com/pentergust): Главный суетолог.
- [@Roman12e](https://github.com/Roman12e): Лучший маркетолог.
- [@Wst-dev](https://github.com/Wst-dev): Мощный разработчик.
- [@Geogarti](https://github.com/Geogarti): Маэстро баз данных.

## Поддержка

При желании вы можете помочь развитию проекта согласно лицензии `GPL-3.0-or-later`.

Мы будем очень рады вашей поддержке.
