from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def paid_keyboard():
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(text="Оплатил", callback_data="paid"),
        InlineKeyboardButton(text="Отмена", callback_data="cancel_payment")
    )

    return markup
