import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.dispatchers import dp
from environment.utils import Env
from db.utils import db

async def on_startup():
    await db.create_all()

async def main() -> None:
    bot = Bot(token=Env.bot.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
