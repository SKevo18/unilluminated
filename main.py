import asyncio
from triedy.herna_slucka import HernaSlucka


async def main():
    await HernaSlucka.spusti()


if __name__ == "__main__":
    asyncio.run(main())
else:
    asyncio.create_task(main())
