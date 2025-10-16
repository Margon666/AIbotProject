import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import openai

load_dotenv()
BOT_TOKEN=os.getenv("BOT_TOKEN")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Не найден BOT_TOKEN или OPENAI_API_KEY в .env файле!")

os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY

bot=Bot(token=BOT_TOKEN)
dp=Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Привет! 🤖 Я GPT-бот на OpenAI. Напиши вопрос!")
@dp.message()

async def chat(message: types.Message):
    user_input=message.text.strip()
    await message.answer("⏳ Думаю...")
    try:
        response=openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный помощник."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=500
        )
        reply=response.choices[0].message.content
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"⚠️ Ошибка OpenAI: {e}")

async def main():
    print("🚀 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
