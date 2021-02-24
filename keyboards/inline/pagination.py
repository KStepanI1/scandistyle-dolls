from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

show_item_cd = CallbackData("show_item", "page", "item_id")
pagination_cd = CallbackData("paginator", "key", "page")


async def get_pages_keyboard(array, page: int = 1):
    key = "items"
    markup = InlineKeyboardMarkup(row_width=1)
    MAX_ITEMS_PER_PAGE = 5
    first_item_index = (page - 1) * MAX_ITEMS_PER_PAGE
    last_item_index = page * MAX_ITEMS_PER_PAGE

    sliced_array = array[first_item_index:last_item_index]
    item_buttons = list()

    for item in sliced_array:
        button_text = f"{item.name}"
        if item.price == 0:
            button_text = f"{item.name} - Бесплатно"
        item_buttons.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=show_item_cd.new(page=page, item_id=item.id),
            )
        )
    pages_buttons = list()

    first_page = 1

    if len(array) % MAX_ITEMS_PER_PAGE == 0:
        max_page = len(array) // MAX_ITEMS_PER_PAGE
    else:
        max_page = len(array) // MAX_ITEMS_PER_PAGE + 1

    previous_page = page - 1
    previous_page_text = f" < "

    if previous_page >= first_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_cd.new(key=key,
                                                page=previous_page)
            )
        )
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=" - ",
                callback_data=pagination_cd.new(key=key,
                                                page="current_page")
            )
        )

    next_page = page + 1
    next_page_text = f" > "

    if next_page <= max_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_cd.new(key=key,
                                                page=next_page)
            )
        )
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=" - ",
                callback_data=pagination_cd.new(key=key,
                                                page="current_page")
            )
        )

    for button in item_buttons:
        markup.insert(button)

    markup.row(*pages_buttons)
    return markup
