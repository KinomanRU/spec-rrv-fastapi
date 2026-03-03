# TODO: Напишите асинхронную программу, которая запускает n асинхронных функции.
#  n - задайте самостоятельно.
#  Каждая функция должна возвращать случайное целое число в диапазоне от 0 до 10
#  и выполняться за случайное время от 1 до 5 секунд
#  После завершения всех функций найдите сумму всех полученных результатов и выведите её на экран.

import asyncio
import random

N = 3


async def get_random_int() -> int:
    await asyncio.sleep(random.randint(1, 5))
    n = random.randint(0, 10)
    print(f"{n=}")
    return n


async def main():
    results = await asyncio.gather(*[get_random_int() for _ in range(N)])
    print(f"SUM of n is {sum(results)}")


if __name__ == "__main__":
    asyncio.run(main())
