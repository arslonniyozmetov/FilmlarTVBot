from aiogram import Dispatcher
from loader import dp
from .throttling import ThrottlingMiddleware
# from .obuna import BaseMiddleware

if __name__ == "middlewares":
    # dp.middleware.setup(BaseMiddleware())  # ob'ekt sifatida
    dp.middleware.setup(ThrottlingMiddleware())  # ob'ekt sifatida