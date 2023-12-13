"""Обработчик reply сообщения"""

from aiogram import F, Router, types

from src.config import LOGER
from src.static.answers import CreateInvoice, UserAnswer, CreateClaim
from src.telebot.buttons_fab import Buttons
from src.database.crud import InvoiceORM, UserORM
from src.database.schemas import GetInvoice
from src.database.redisdb import MyRedisCli

router = Router()
router.message.filter(F.reply_to_message.from_user.is_bot == True)


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateInvoice.DESCRIPTION.value,
)
async def invoice_description(message: types.Message):
    """принимает описание накладной"""
    LOGER.info(f"{message.text}")
    user = await UserORM().get_user(message.from_user.id)
    await MyRedisCli.insert_data(
        f"I{message.from_user.id}",
        description=message.text,
        user_id=user.id
    )
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
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
    await MyRedisCli.update_data(
        f"I{message.from_user.id}",
        weight=message.text
    )
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
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
    await MyRedisCli.update_data(
        f"I{message.from_user.id}",
        height=message.text
    )
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
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
    await MyRedisCli.update_data(
        f"I{message.from_user.id}",
        length=message.text
    )
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
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
    await MyRedisCli.update_data(
        f"I{message.from_user.id}",
        width=message.text
    )
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
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
    await MyRedisCli.update_data(
        f"I{message.from_user.id}",
        where_from=message.text
    )
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
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
    await MyRedisCli.update_data(
        f"I{message.from_user.id}",
        to_location=message.text
    )
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
    await message.answer(
        text=CreateInvoice.PAYMENT.value,
        reply_markup=Buttons.payment_type_buttons()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateClaim.INVOICE_ID.value,
)
async def claim_invoice_id(message: types.Message):
    """принимает описание накладной"""
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
    user = await UserORM().get_user_with_invoices(message.from_user.id)
    invoices_id = [i.id for i in user.invoices]
    if int(message.text) in invoices_id:
        await MyRedisCli.insert_data(
            f"C{message.from_user.id}",
            invoice_id=int(message.text),
        )
        await message.answer(
            CreateClaim.EMAIL.value,
            reply_markup=Buttons.break_claim()
        )
    else:
        await message.answer("Не понял ваше сообщение")
        await message.answer(
            text=CreateClaim.INVOICE_ID.value,
            reply_markup=Buttons.break_claim()
        )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateClaim.EMAIL.value,
)
async def claim_email(message: types.Message):
    """принимает описание накладной"""
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
    await MyRedisCli.update_data(
        f"C{message.from_user.id}",
        email=message.text
    )
    await message.answer(
        text=CreateClaim.DESCRIPTION.value,
        reply_markup=Buttons.break_claim()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateClaim.DESCRIPTION.value,
)
async def claim_description(message: types.Message):
    """принимает описание накладной"""
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
    await MyRedisCli.update_data(
        f"C{message.from_user.id}",
        description=message.text
    )
    await message.answer(
        text=CreateClaim.REQUIRED_AMOUNT.value,
        reply_markup=Buttons.break_claim()
    )


@LOGER.catch
@router.message(
    F.reply_to_message.text == CreateClaim.REQUIRED_AMOUNT.value,
)
async def claim_required_amount(message: types.Message):
    """принимает описание накладной"""
    LOGER.info(f"{message.text}")
    await message.bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message.reply_to_message.message_id,
        reply_markup=None
    )
    await MyRedisCli.update_data(
        f"C{message.from_user.id}",
        required_amount=message.text
    )
    await message.answer(
        text=CreateClaim.PHOTOS.value,
        reply_markup=Buttons.break_claim()
    )


# @LOGER.catch
# @router.message(
#     F.reply_to_message.text == CreateClaim.PHOTOS.value,
# )
# async def claim_photos(message: types.Message):
#     """принимает фотографии для претензии"""
#     pass


@LOGER.catch
@router.message(
    F.reply_to_message.text == UserAnswer.GET_INVOICE.value
)
async def get_current_invoice(message: types.Message):
    """Обработка запросана конкретную накладную"""
    try:
        invoice_id = int(message.text)
        if isinstance(invoice_id, int):
            res = await InvoiceORM().get_invoice(int(message.text))
            user = await UserORM().get_user(message.from_user.id)
            if res:
                if res.user_id == user.id:
                    result = GetInvoice.model_validate(res)
                    LOGER.info(result)
                    await message.answer(text=f"{result}")
    except ValueError:
        await message.answer(text="Непонял ваще сообщение")
