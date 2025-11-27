import asyncio
from aiogram import Bot
from src.config import TG_TOKEN
from src.db import dp


import src.handlers

bot = Bot(token=TG_TOKEN)


async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
