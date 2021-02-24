from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asgiref.sync import sync_to_async

from utils.db_api.quick_commands.commands_item import get_items, get_item

menu_cd = CallbackData("show_menu", "item_id")
buy_item_cd = CallbackData("buy", "is_free", "item_id")


def make_callback_data(item_id="0"):
    return menu_cd.new(item_id=item_id)


async def items_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)

    items = await get_items()
    for item in items:
        button_text = f"{item.name}"
        callback_data = make_callback_data(item_id=item.id)
        markup.insert(
            InlineKeyboardButton(
                text=button_text, callback_data=callback_data)
        )

    return markup


async def item_keyboard(page, item_id):
    markup = InlineKeyboardMarkup(row_width=2)
    item = await get_item(item_id)
    if item.price == 0:
        markup.insert(InlineKeyboardButton(
            text=f"Получить",
            callback_data=buy_item_cd.new(is_free="True", item_id=item_id)
        )
        )
    else:
        markup.insert(
            InlineKeyboardButton(
                text=f"Купить",
                callback_data=buy_item_cd.new(is_free="False", item_id=item_id)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=f"К товарам",
            callback_data=f"back_to_items:{page}"
        )
    )
    return markup
