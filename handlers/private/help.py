from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.default.help_keyboard import help_keyboard
from loader import dp


@dp.message_handler(Command('help'), state="*")
async def show_help_keyboard(message: types.Message, state: FSMContext):
    await message.answer(text="Внимательно слушаю", reply_markup=help_keyboard)


@dp.message_handler(text="Способы оплаты")
async def answer_payment_method(message: types.Message):
    pass


@dp.message_handler(text="Связь со мной")
async def answer_contact(message: types.Message):
    pass
