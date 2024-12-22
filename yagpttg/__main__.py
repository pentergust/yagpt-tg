"""Файл запуска бота.

Для запуска бота:

```sh
py -m yagpttg
```
"""

import asyncio

from yagpttg.bot import main

if __name__ == "__main__":
    asyncio.run(main())
