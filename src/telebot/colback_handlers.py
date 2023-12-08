"""Хендлер для обработки нажатий на кнопки"""

from aiogram import Router, types, F

from src.static.buttons import UserButtons
from src.static.answers import CreateInvoice, UserAnswer
from src.telebot.buttons_fab import Buttons
from src.config import LOGER

router = Router()


@router.callback_query(F.data == UserButtons.CR_INVOICE.name)
async def create_invoice(callback: types.CallbackQuery):
    """Обработка запуска генерации накладной"""
    await callback.message.answer(
        text=CreateInvoice.DESCRIPTION.value,
        reply_markup=Buttons.break_invoice()
    )


@LOGER.catch
@router.callback_query(F.data == UserButtons.BREAK_INVOICE.name)
async def break_invoice(callback: types.CallbackQuery):
    """Логика дропа генерации накладной"""
    await callback.message.answer(text=CreateInvoice.DROP.value)
    await callback.message.answer(
        text=UserAnswer.START.value,
        reply_markup=Buttons.user_buttons()
    )
