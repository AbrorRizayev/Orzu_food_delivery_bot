from os import getenv

from aiogram import Dispatcher

from bot.handlers.branches import branch_router
from bot.handlers.main import main_router
from bot.handlers.menu import menu_router

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_routers(main_router, branch_router, menu_router)
