import asyncio
import sqlite3
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat

load_dotenv()
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
GIGA_TOKEN = os.getenv("GIGACHAT_TOKEN")

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
    return [{"role": r[0], "content": r[1]} for r in rows]


def clear_history(user_id: int):
    cursor.execute("DELETE FROM dialogs WHERE user_id=?", (user_id,))
    conn.commit()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    welcome_text = """
    Привет! Я бот-ассистент по программированию и тайм-менеджменту.

    Я могу помочь вам с:
    - Вопросами по программированию (Python, JavaScript, и др.)
    - Решением проблем с кодом
    - Советами по тайм-менеджменту и продуктивности
    - Планированием задач и организации времени

    Доступные команды:
    /start - показать это сообщение
    /clear - очистить историю диалога
    /help - показать справку
    """
    await message.answer(welcome_text)


@dp.message(Command("help"))
async def help_command(message: types.Message):
    help_text = """
    Я специализируюсь на двух темах:

    📚 Программирование:
    - Помощь с кодом
    - Объяснение концепций
    - Решение ошибок
    - Рекомендации по инструментам

    ⏰ Тайм-менеджмент:
    - Планирование времени
    - Организация задач
    - Повышение продуктивности
    - Методы работы

    Если ваш вопрос не по этим темам, я отвечу: "Я не могу ответить на это сообщение"

    Команды:
    /clear - очистить историю диалога
    """
    await message.answer(help_text)


@dp.message(Command("clear"))
async def clear_command(message: types.Message):
    clear_history(message.from_user.id)
    await message.answer("История диалога очищена! ✅")


@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text

    save_message(user_id, "user", user_message)

    history = get_history(user_id)

    system_prompt = """Ты - опытный ассистент, специализирующийся на программировании и тайм-менеджменте. 
    Ты отвечаешь только на вопросы, связанные с:
    1. Программирование: код, алгоритмы, языки программирования, технологии
    2. Тайм-менеджмент: планирование времени, продуктивность, организация задач

    На любые другие темы ты отвечаешь строго: "Я не могу ответить на это сообщение"

    Отвечай кратко, по делу и полезно."""

    messages = [{"role": "system", "content": system_prompt}] + history

    try:
        response = giga.chat(Chat(messages=messages))
        bot_response = response.choices[0].message.content

        save_message(user_id, "assistant", bot_response)

        await message.answer(bot_response)

    except Exception as e:
        print(f"Ошибка при обращении к GigaChat: {e}")
        await message.answer("Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже.")


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())