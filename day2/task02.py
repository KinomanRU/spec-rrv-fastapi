# TODO: Создайте 4 корутины, каждая из которых возвращает строку.
#  Запустите их параллельно и соберите результаты в список.

import asyncio
import random

STRINGS = (
    "Apple",
    "Orange",
    "Kiwi",
    "Lemon",
    "Pineapple",
    "Watermelon",
    "Melon",
    "Mango",
)


async def get_random_string() -> str:
    return random.choice(STRINGS)


async def main():
    results = await asyncio.gather(*[get_random_string() for _ in range(4)])
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
