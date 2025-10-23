import asyncio
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from gigachat import GigaChat
from dotenv import load_dotenv
from gigachat.models import Chat
import os

load_dotenv()
TG_TOKEN=os.getenv("TELEGRAM_TOKEN")
GIGA_TOKEN=os.getenv("GIGACHAT_TOKEN")

DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
bot=Bot(token=TG_TOKEN)
dp=Dispatcher()

giga = GigaChat(credentials=GIGA_TOKEN, verify_ssl_certs=False)

conn = psycopg2.connect(host="https://st.timeweb.com/cloud-static/ca.crt",prot="")
conn.commit()

def get_connetuin():
    return psycopg2.connect(host=DB_HOST,port=DB_PORT,dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD)

def init_db():
    conn=get_connetion()
    cursor=conn.cursor()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот, который общается через GigaChat. Напиши что-нибудь 😉")

@dp.message()
async def chat_handler(message: types.Message):
    user_id=message.from_user.id
    user_text=message.text

    save_message(user_id,"user",user_text)

    history=get_history(user_id)

    chat_request=Chat(messages=history)
    response=giga.chat(chat_request)
    answer=response.choices[0].message.content

    save_message(user_id,"assistant", answer)

    await message.answer(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())