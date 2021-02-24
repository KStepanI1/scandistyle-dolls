import logging

from aiogram import Dispatcher

from data import config


async def on_startup_notify(dp: Dispatcher):

    for superuser in config.SUPERUSER_ID:
        try:
            await dp.bot.send_message(superuser, "Бот запущен")

        except Exception as err:
            logging.info(err)
