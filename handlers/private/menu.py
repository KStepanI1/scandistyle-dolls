from contextlib import suppress
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, InputFile
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound, MessageNotModified
from asgiref.sync import sync_to_async

from keyboards.inline.menu_keyboard import menu_cd, \
    items_keyboard, item_keyboard
from keyboards.inline.pagination import get_pages_keyboard, show_item_cd, pagination_cd
from loader import dp, bot
from utils.db_api.quick_commands.commands_item import get_item, get_items


@dp.message_handler(Command("menu"), state="*")
async def show_menu(message: types.Message):
    await list_items(message)


async def list_items(message: types.Message, **kwargs):
    items = await get_items()
    markup = await get_pages_keyboard(items)
    await message.answer(text="<b>Список мастер-классов</b>", reply_markup=markup)


@dp.callback_query_handler(pagination_cd.filter(key="items"))
async def show_chosen_page(message: Union[types.CallbackQuery, types.Message], state: FSMContext,
                           callback_data: dict = None):
    items = await get_items()
    if isinstance(message, types.CallbackQuery):
        call = message
        try:
            current_page = int(callback_data.get("page"))
            await call.answer(text=f"Страница: {current_page}")
            markup = await get_pages_keyboard(items, page=current_page)
            with suppress(MessageNotModified):
                await call.message.edit_reply_markup(
                    reply_markup=markup
                )
        except ValueError:
            await call.answer(text="Текущая страница")
    elif isinstance(message, types.Message):
        data = await state.get_data()
        page = data.get("page")
        await state.finish()
        if not page:
            page = 1
        markup = await get_pages_keyboard(items, page=page)
        await message.answer(text="<b>Список мастер-классов</b>", reply_markup=markup)


@dp.callback_query_handler(show_item_cd.filter(), state="*")
async def show_item(callback: CallbackQuery, callback_data: dict):
    item_id = callback_data.get("item_id")
    current_page = int(callback_data.get("page"))
    markup = await item_keyboard(current_page, item_id)
    item = await get_item(item_id)
    await callback.answer(text=f"Товар: {item.name}")
    text = f'''
<b>Название:</b> 
{item.name}

<b>Описание:</b> 
{item.description}

<b>Цена:</b> {item.price}
'''
    photo = item.photo.file_id
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer_photo(photo=photo, caption=text, reply_markup=markup)


@dp.callback_query_handler(text_contains="back_to_items", state="*")
async def show_list_items(call: types.CallbackQuery, state: FSMContext):
    current_page = int(call.data.split(":")[-1])
    await call.answer(text=f"Страница: {current_page}")
    await state.update_data(page=current_page)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    await show_chosen_page(call.message, state)
