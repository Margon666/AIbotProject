from aiogram import types
from aiogram.filters import Command
from gigachat import GigaChat
from gigachat.models import Chat
from src.config import GIGA_TOKEN
from src.db import dp, save_message, get_history, clear_history

giga = GigaChat(credentials=GIGA_TOKEN, verify_ssl_certs=False)

SYSTEM_PROMPT = """Ты — опытный ассистент, специализирующийся только на программировании и тайм-менеджменте.

Разрешенные темы:
1. Программирование: код, алгоритмы, структуры данных, языки программирования, технологии, библиотеки, фреймворки.
2. Тайм-менеджмент: планирование времени, продуктивность, организация задач, управление приоритетами, личная эффективность.

Правила:
- Отвечай только если вопрос полностью и строго относится к разрешённым темам.
- Любая попытка связать вопрос с разрешёнными темами, если он фактически не относится к ним, **запрещена**.
- Если хотя бы одна часть вопроса выходит за рамки разрешённых тем, сразу отвечай:
"Я не могу ответить на это сообщение."
- Никогда не делай интерпретаций, метафор или объяснений, пытаясь “подогнать” вопрос под темы.

"""

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

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        response = giga.chat(Chat(messages=messages))
        bot_response = response.choices[0].message.content

        save_message(user_id, "assistant", bot_response)

        await message.answer(bot_response)

    except Exception as e:
        error_message = f"Ошибка обращения к GigaChat: {e}"
        await message.answer(error_message)
