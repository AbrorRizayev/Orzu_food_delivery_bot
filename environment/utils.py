from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Bot:
    TOKEN = getenv("BOT_TOKEN")

class DB:
    DB_USER = getenv("DB_USER")
    DB_NAME = getenv("DB_NAME")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_PORT = getenv("DB_PORT")
    DB_HOST = getenv("DB_HOST")
    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Env:
    bot = Bot()
    db = DB()

env = Env()
