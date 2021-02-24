from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

help_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Способы оплаты")
        ],
        [
            KeyboardButton(text="Связь со мной")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)