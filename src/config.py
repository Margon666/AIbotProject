import os
from dotenv import load_dotenv


load_dotenv()
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
GIGA_TOKEN = os.getenv("GIGACHAT_TOKEN")

