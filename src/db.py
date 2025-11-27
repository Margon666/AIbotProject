import sqlite3
from aiogram import Dispatcher, types
from aiogram.filters import Command

dp = Dispatcher()

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
    cursor.execute(
        "INSERT INTO dialogs (user_id, role, message) VALUES (?, ?, ?)",
        (user_id, role, message)
    )
    conn.commit()


def get_history(user_id: int):
    cursor.execute(
        "SELECT role, message FROM dialogs WHERE user_id=? ORDER BY rowid",
        (user_id,)
    )
    rows = cursor.fetchall()
    return [{"role": r, "content": m} for r, m in rows]


def clear_history(user_id: int):
    cursor.execute("DELETE FROM dialogs WHERE user_id=?", (user_id,))
    conn.commit()
