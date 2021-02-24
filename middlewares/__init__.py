from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from loader import dp
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LoggingMiddleware())
