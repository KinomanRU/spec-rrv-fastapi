# TODO: Создайте корутину, которая ждет 5 секунд.
#  Запустите ее как задачу и отмените ее через 2 секунды.

import asyncio


async def wait_5_sec() -> None:
    await asyncio.sleep(5)
    print("Task completed")


async def main():
    task = asyncio.create_task(wait_5_sec())
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Task cancelled")


if __name__ == "__main__":
    asyncio.run(main())
