"""Обработчик reply сообщения"""

from aiogram import F, Router, types

from src.config import LOGER
from src.static.answers import CreateInvoice, UserAnswer
from src.telebot.buttons_fab import Buttons

router = Router()
router.message.filter(F.reply_to_message.from_user.is_bot == True)


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateInvoice.DESCRIPTION.value,
)
async def invoice_description(message: types.Message):
    """принимает описание накладной"""
    LOGER.info(f"{message.text}")
    await message.answer(
        CreateInvoice.WEIGHT.value,
        reply_markup=Buttons.break_invoice()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateInvoice.WEIGHT.value,
)
async def invoice_weight(message: types.Message):
    """принимает вес накладной"""
    LOGER.info(f"{message.text}")
    await message.answer(
        CreateInvoice.HEIGHT.value,
        reply_markup=Buttons.break_invoice()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateInvoice.HEIGHT.value,
)
async def invoice_height(message: types.Message):
    """принимает высоту накладной"""
    LOGER.info(f"{message.text}")
    await message.answer(
        CreateInvoice.LENGTH.value,
        reply_markup=Buttons.break_invoice()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateInvoice.LENGTH.value,
)
async def invoice_length(message: types.Message):
    """принимает длину накладной"""
    LOGER.info(f"{message.text}")
    await message.answer(
        CreateInvoice.WIDTH.value,
        reply_markup=Buttons.break_invoice()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateInvoice.WIDTH.value,
)
async def invoice_width(message: types.Message):
    """принимает ширину накладной"""
    LOGER.info(f"{message.text}")
    await message.answer(
        CreateInvoice.WHERE_FROM.value,
        reply_markup=Buttons.break_invoice()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateInvoice.WHERE_FROM.value,
)
async def invoice_where_from(message: types.Message):
    """прнимает адрес отправки накладной"""
    LOGER.info(f"{message.text}")
    await message.answer(
        CreateInvoice.TO_LOCATION.value,
        reply_markup=Buttons.break_invoice()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateInvoice.TO_LOCATION.value,
)
async def invoice_to_location(message: types.Message):
    """принимает адрес доставки накладной"""
    LOGER.info(f"{message.text}")
    await message.answer(
        CreateInvoice.PAYMENT.value,
        reply_markup=Buttons.break_invoice()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateInvoice.PAYMENT.value,
)
async def invoice_payment(message: types.Message):
    """принимает способ оплаты накладной"""
    LOGER.info(f"{message.text}")
    await message.answer("Конец обработки")
    await message.answer(
        UserAnswer.START.value,
        reply_markup=Buttons.user_buttons()
    )
