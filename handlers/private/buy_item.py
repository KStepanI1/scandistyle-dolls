import logging

import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink, hcode

from data import config
from django_project.usersmanage.models import Purchase
from keyboards.inline.menu_keyboard import buy_item_cd
from keyboards.inline.payment_keyboard import paid_keyboard
from loader import dp
from utils.db_api.quick_commands.commands_item import get_item
from utils.db_api.quick_commands.commands_user import select_user
from utils.qiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.callback_query_handler(buy_item_cd.filter(is_free="False"), state="*")
async def enter_buy(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(text="Покупка товара")
    user = await select_user(call.from_user.id)
    if not user.email:
        await call.message.answer(
            "Перед началом оплаты нужно указать вашу <b>электронную почту</b>\n"
            "На нее будут приходить оплаченые мастер классы\n"
            "Почта вводится один раз\n\n"
            "Используйте /email для того чтобы указать почту"
        )
        return
    else:
        item_id = callback_data.get("item_id")
        item = await get_item(item_id)

        purchase = Purchase()
        purchase.buyer_id = user.id
        purchase.item_id_id = int(item_id)
        purchase.receiver = call.from_user.full_name

        payment = Payment(amount=item.price)
        payment.create()

        markup = await paid_keyboard()

        await call.message.answer(
            "\n".join(
                [
                    f"Оплатите не менее {item.price:.2f} ₽ по ссылке ниже",
                    "Обязательно проверьте, что указан ID платежа:",
                    hcode(payment.id),
                    f"Убедитесь в правильности введенного вами email адресса {user.email}",
                    "",
                    hlink("Нажмите, чтобы перейти к оплате", url=payment.invoice),
                ]
            ),
            reply_markup=markup
        )
        await state.update_data(payment=payment, item=item)
        await state.update_data(user_id=user.user_id, purchase=purchase)
        await state.set_state("qiwi")


@dp.callback_query_handler(text_contains="cancel_payment", state="qiwi")
async def cancel_payment(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Отменено")
    await state.finish()


async def sending_paid_item(item, user):
    sender_email = config.EMAIL_ADDRESS
    receiver_email = user.email
    password = config.EMAIL_PASSWORD
    port = 465
    path_to_file = "data/media/"
    body = f'''\
Здравствуйте!

Вы приобрели мастер-класс {item.name} в телеграмм боте @scandistyle_dolls_bot.
    
К этому письму прилагается PDF файл с купленным Вами мастер-классом. 
    
Если по какой-то причине у Вас не получается загрузить или открыть 
данный файл, пожалуйста, свяжитесь со мной в Инстаграм 
(@scandistyle_dolls) или по почте niusha1695@gmail.com.
    
Благодарю за приобретение мастер-класса! Вяжите с удовольствием.
    
С уважением,
    
Надежда Юхлина
@scandistyle_dolls'''
    message = MIMEMultipart("alternative")
    message["Subject"] = "Покупка в Scandistyle Dolls"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(body, "plain"))

    filename = item.file.name
    print(path_to_file + filename)
    with open(path_to_file + filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


@dp.callback_query_handler(text_contains="paid", state="qiwi")
async def approve_payment(call: CallbackQuery, state: FSMContext):
    await call.answer(text="Проверка оплаты")
    data = await state.get_data()
    payment = data.get("payment")
    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.message.answer("Транзакция не найдена")
        return
    except NotEnoughMoney:
        await call.message.answer("Оплаченая сумма меньше необходимой")
        return
    else:
        purchase = data.get("purchase")
        item = data.get("item")
        user_id = data.get("user_id")
        user = await select_user(user_id)
        purchase.amount = item.price
        purchase.email = user.email
        purchase.save()
        paid_text = f'''\
Товар успешно оплачен!
    
Мастер-класс был отправлен по почте {user.email}
Если вы не обнаружите товар на почте в течение 5-10 минут, 
свяжитесь со мной в {hlink("Телеграм", "https://t.me/n_iukhlina")} или {hlink("Инстаграм", "https://www.instagram.com/scandistyle_dolls/")}.
    
С уважением, 
Надежда Юхлина
'''
        try:
            await call.message.edit_text(paid_text, disable_web_page_preview=True)
        except Exception as err:
            logging.error(err)
            await call.message.answer(paid_text, disable_web_page_preview=True)

        await sending_paid_item(item, user)
        await state.finish()


@dp.callback_query_handler(buy_item_cd.filter(is_free="True"), state="*")
async def send_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user = await select_user(call.from_user.id)
    await call.answer(text="Отправка товара")
    if not user.email:
        await call.message.answer(
            "Перед началом оплаты нужно указать вашу <b>электронную почту</b>\n"
            "На нее будут приходить оплаченые мастер классы\n"
            "Почта вводится один раз\n\n"
            "Используйте /email для того чтобы указать почту"
        )
        return
    else:
        item_id = callback_data.get("item_id")
        item = await get_item(item_id)
        send_text = f'''\
Товар успешно отправлен!

Мастер-класс был отправлен по почте {user.email}
Если вы не обнаружите товар на почте в течение 5-10 минут, 
свяжитесь со мной в {hlink("Телеграм", "https://t.me/n_iukhlina")} или {hlink("Инстаграм", "https://www.instagram.com/scandistyle_dolls/")}.

С уважением, 
Надежда Юхлина'''
        try:
            await call.message.edit_text(send_text, disable_web_page_preview=True)
        except Exception as err:
            logging.error(err)
            await call.message.answer(send_text, disable_web_page_preview=True)

        await sending_paid_item(item, user)
    await state.finish()
