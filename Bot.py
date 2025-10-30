import asyncio
import sqlite3
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat

load_dotenv()
TG_TOKEN=os.getenv("TELEGRAM_TOKEN")
GIGA_TOKEN=os.getenv("GIGACHAT_TOKEN")


bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

giga = GigaChat(credentials=GIGA_TOKEN, verify_ssl_certs=False)

conn = sqlite3.connect("dialogs.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS dialogs (
    user_id INTEGER,
    role TEXT,
    message TEXT
)
""")
conn.commit()


def save_message(user_id: int, role: str, message: str):
    cursor.execute("INSERT INTO dialogs (user_id, role, message) VALUES (?, ?, ?)",
                   (user_id, role, message))
    conn.commit()


def get_history(user_id: int):
    cursor.execute("SELECT role, message FROM dialogs WHERE user_id=? ORDER BY rowid", (user_id,))
    rows = cursor.fetchall()
    return [{"role": r, "content": m} for r, m in rows]


def clear_history(user_id: int):
    cursor.execute("DELETE FROM dialogs WHERE user_id=?", (user_id,))
    conn.commit()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! 👋 Я бот, который общается через GigaChat от Сбера.\n"
        "Напиши мне что-нибудь!\n\n"
    )


@dp.message()
async def chat_handler(message: types.Message):
    user_id=message.from_user.id
    user_text=message.text

    save_message(user_id, "user", user_text)
    history=get_history(user_id)
    filtered_history = [m for m in history if m["role"] in ("user", "assistant")]
    try:
        chat_request = Chat(
            messages=[
                         {"role": "system",
                          "content": "Ты — фильтр политических тем. Если запрос связан с политикой отвечай только 'Да' и ничего больше"},
                         {"role": "user", "content": user_text}
                     ] + filtered_history
        )
        response=giga.chat(chat_request)
        answer=response.choices[0].message.content
    except Exception as e:
        answer = f"Ошибка использования GigaChat: {e}"
    save_message(user_id, "assistant", answer)
    await message.answer(answer)

async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())