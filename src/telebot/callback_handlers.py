"""Хендлер для обработки нажатий на кнопки"""

from aiogram import Router, types, F

from src.database.crud import UserORM
from src.static.buttons import UserButtons
from src.static.answers import CreateInvoice, UserAnswer
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
