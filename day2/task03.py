# TODO: Создайте несколько асинхронных задач с разными задержками.
#  Используйте asyncio.as_completed() для обработки результатов задач по мере их завершения.
#  Выведите результаты каждой задачи сразу после ее завершения.

import asyncio
import random


async def some_longop(task_id: int, delay: int) -> str:
    await asyncio.sleep(delay)
    return f"Task {task_id} completed in {delay} seconds."


async def main():
    n = random.randint(1, 5)
    print(f"Will be planned for {n} task(s)")
    for task in asyncio.as_completed(
        [some_longop(i + 1, random.randint(1, 5)) for i in range(n)]
    ):
        print(await task)


if __name__ == "__main__":
    asyncio.run(main())
