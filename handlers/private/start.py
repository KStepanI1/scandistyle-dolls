from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.utils.markdown import hlink

from loader import dp
from utils.db_api.quick_commands import commands_user as commands
from utils.db_api.quick_commands.commands_user import update_user_email


@dp.message_handler(CommandStart(), state="*")
async def show_greeting(message: types.Message):
    username = message.from_user.username
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    await commands.add_user(user_id=user_id,
                            full_name=full_name,
                            username=username)
    text = f'''\
<b>Добро пожаловать в магазин мастер-классов ScandistyleDolls!</b>

Здесь Вы можете приобрести любой из моих мастер-классов. Для этого нажмите сюда /menu.

Узнать про способы оплаты можно, нажав сюда /help.

Если у Вас возникли вопросы, свяжитесь со мной в {hlink("Телеграм", "https://t.me/n_iukhlina")} или {hlink("Инстаграм", "https://www.instagram.com/scandistyle_dolls/")}.

Приятных покупок!

С уважением, 
Надежда Юхлина
'''
    await message.answer(text=text, disable_web_page_preview=True)


@dp.message_handler(Command('email'), state="*")
async def get_email(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Хорошо. Введи свой email и я его запишу\n\n"
                         "<b>Важно:</b> Следующее сообщение будет записано как Ваш email только в том случае, "
                         "если оно будет удовлетворять формату email адреса")
    await state.set_state("email")


@dp.message_handler(state="email", regexp=r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+")
async def save_email(message: types.Message, state: FSMContext):
    await update_user_email(message.from_user.id, message.text)
    await message.answer(f"Ваш email успешно записан как: {message.text}")
    await state.finish()
