from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("get_photo_id"), state="*")
async def ask_photo_name(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Пришли мне фото и я выдам тебе photo file_id")
    await state.set_state("get_photo")


@dp.message_handler(state="get_photo", content_types=types.ContentType.PHOTO)
async def give_photo_file_id(message: types.Message, state: FSMContext):

    photo_file_id = message.photo[-1].file_id

    await message.answer(f"Вот id для присланного фото: {photo_file_id}")
    await state.finish()
