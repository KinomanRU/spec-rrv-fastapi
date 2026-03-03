# TODO: Напишите асинхронную программу, которая отправляет HTTP-запросы к трём различным веб-сайтам:
#  "https://www.yandex.com", "https://www.google.com" и "https://www.python.org".
#  Как только от одного из сайтов будет получен ответ,
#  необходимо отменить выполнение запросов к остальным сайтам
#  и вывести время, затраченное на получение первого ответа.

import asyncio
import time
import aiohttp

URLS = (
    "https://www.yandex.com",
    "https://www.google.com",
    "https://www.python.org",
)


async def get_response_status(url: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return response.status


async def main():
    tasks = []
    for url in URLS:
        tasks.append(asyncio.create_task(get_response_status(url)))
    start = time.perf_counter()
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in done:
        print(
            f"Got status {task.result()} in {time.perf_counter() - start:.2f} seconds. Interrupting other requests..."
        )
    for task in pending:
        task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
