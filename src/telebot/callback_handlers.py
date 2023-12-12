"""Хендлер для обработки нажатий на кнопки"""

from aiogram import Router, types, F

from src.database.crud import UserORM, InvoiceORM
from src.database.models import PaymentType
from src.database.schemas import InsertInvoice
from src.static.buttons import UserButtons
from src.static.answers import CreateInvoice, UserAnswer
from src.database.redisdb import MyRedisCli
from src.telebot.buttons_fab import Buttons
from src.config import LOGER

router = Router()


@LOGER.catch
@router.callback_query(F.data == UserButtons.CR_INVOICE.name)
async def create_invoice(callback: types.CallbackQuery):
    """Обработка запуска генерации накладной"""
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    redis_data = await MyRedisCli.get_data(f"I{callback.from_user.id}")
    LOGER.info(redis_data)
    LOGER.info(callback.from_user.id)
    if redis_data:
        await callback.message.answer(
            text="Кажется у Вас есть незаконченная накладная, хотите продолжить?"
        )
    else:
        await callback.message.answer(
            text=CreateInvoice.DESCRIPTION.value,
            reply_markup=Buttons.break_invoice()
        )


@LOGER.catch
@router.callback_query(F.data == UserButtons.BREAK_INVOICE.name)
async def break_invoice(callback: types.CallbackQuery):
    """Логика дропа генерации накладной"""
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer(text=CreateInvoice.DROP.value)
    await callback.message.answer(
        text=UserAnswer.START.value,
        reply_markup=Buttons.user_buttons()
    )


@LOGER.catch
@router.callback_query(F.data == UserButtons.GET_ARRAY_INVOICES.name)
async def get_array_invoices(callback: types.CallbackQuery):
    """Пользовательский список накладных"""
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    res = await UserORM().get_user_with_invoices(callback.from_user.id)
    result = list(res.invoices)
    if len(result) == 0:
        await callback.message.answer(
            text=f"У вас есть {len(result)} накладных"
        )
        await callback.message.answer(
            text=UserAnswer.START.value,
            reply_markup=Buttons.user_buttons()
        )
    else:
        invoices_id = [i.id for i in result]
        await callback.message.answer(
            text=UserAnswer.ANSWER_INVOICE.value
        )
        await callback.message.answer(
            text=f"{invoices_id}"
        )
        await callback.message.answer(
            text=UserAnswer.GET_INVOICE.value
        )


@LOGER.catch
@router.callback_query(F.data.in_(
    (PaymentType.CASH.name, PaymentType.DC.name, PaymentType.SBP.name)
))
async def create_payment(callback: types.CallbackQuery):
    """Обработка типа оплаты и запись результатов создания накладной в БД"""
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await MyRedisCli.update_data(
        f"I{callback.from_user.id}",
        payment=callback.data
    )
    invoice = await MyRedisCli.get_data(f"I{callback.from_user.id}")
    res = InsertInvoice(**invoice)
    a = await InvoiceORM().insert_invoice(dict(res))
    if a:
        await callback.message.answer("Конец обработки")
        await callback.message.answer(
            UserAnswer.START.value,
            reply_markup=Buttons.user_buttons()
        )
    else:
        await callback.message.answer("Что то пошло не так, заполните накладную заново")
        await callback.message.answer(
            UserAnswer.START.value,
            reply_markup=Buttons.user_buttons()
        )
