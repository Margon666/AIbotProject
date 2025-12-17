import sys
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / "dialogs.db"


def connect_db():
    if not db_path.exists():
        print(f"База данных не найдена")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def list_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT user_id FROM dialogs")
    users = cursor.fetchall()

    conn.close()

    print("Пользователи\n")
    for u in users:
        print(f"- {u['user_id']}")


def show_history(user_id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, message FROM dialogs WHERE user_id=? ORDER BY rowid",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    print(f"\nИстория диалога пользователя {user_id}\n")
    print("-" * 30)
    for r in rows:
        if r["role"] == "user":
            role = "user"
        else:
            role = "AI"
        print(f"{role}: {r['message']}\n")
    print("-" * 30)


def print_help():
    print("""
Admin CLI для управления диалогами

Команды:
  users
      Показать всех пользователей

  history <user_id>
      Показать диалоги пользователя

""")

def main():
    if len(sys.argv)<2:
        print_help()
        return
    cmd=sys.argv[1].lower()

    if cmd=="users":
        list_users()
    elif cmd=="history":
        show_history(int(sys.argv[2]))
    else:
        print(f"Неверная команда: {cmd}")
        print_help()

if __name__=="__main__":
    main()