from gigachat import GigaChat
from gigachat.models import Chat
from aiogram import types
from src.config import GIGA_TOKEN
from src.db import dp, get_history, save_message

giga = GigaChat(credentials=GIGA_TOKEN, verify_ssl_certs=False)


@dp.message()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text

    save_message(user_id, "user", user_text)
    history = get_history(user_id)
    filtered_history = [m for m in history if m["role"] in ("user", "assistant")]
    system_message = {
        "role": "system",
        "content": (
            "Ты — интеллектуальный ассистент, работающий в Telegram-боте через GigaChat.\n"
            "Ты ведёшь диалоги с пользователями, при этом контекст их сообщений сохраняется "
            "в локальной базе данных SQLite под названием 'dialogs.db'.\n\n"
            "Структура таблицы 'dialogs' следующая:\n"
            " - user_id (INTEGER) — уникальный идентификатор пользователя Telegram,\n"
            " - role (TEXT) — роль участника диалога ('user' или 'assistant'),\n"
            " - message (TEXT) — текст сообщения.\n\n"
            "Диалоги загружаются в память перед каждым новым ответом, чтобы сохранять контекст.\n\n"
            "Ты должен отвечать только на вопросы, связанные с:\n"
            "1. Программированием (Python, JavaScript, алгоритмы, базы данных и т.п.)\n"
            "2. Тайм-менеджментом (планирование, продуктивность, управление временем).\n\n"
            "Если пользователь задаёт вопрос вне этих тем, отвечай строго фразой:\n"
            "'Извини, я могу отвечать только на вопросы о программировании и тайм-менеджменте.'"
        ),
    }
    try:
        chat_request = Chat(
            messages=[system_message]
            + filtered_history
            + [{"role": "user", "content": user_text}]
        )
        response = giga.chat(chat_request)
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Ошибка использования GigaChat: {e}"
    save_message(user_id, "assistant", answer)
    await message.answer(answer)
