from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("menu", "Список мастер-классов"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("email", "Ввод email адреса"),
    ])