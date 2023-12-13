"""Кнопочная фабрика"""

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.static.buttons import UserButtons, ManagerButtons, InvoiceButtons, ClaimButtons
from src.database.models import PaymentType


class Buttons:
    """Хранитель кнопок"""

    @staticmethod
    def user_buttons():
        """Кнопки для пользователя"""
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text=UserButtons.CR_INVOICE.value,
            callback_data=str(UserButtons.CR_INVOICE.name))
        )
        builder.row(types.InlineKeyboardButton(
            text=UserButtons.CR_CLAIM.value,
            callback_data=str(UserButtons.CR_CLAIM.name))
        )
        builder.row(types.InlineKeyboardButton(
            text=UserButtons.CALL_MANAGER.value,
            callback_data=str(UserButtons.CALL_MANAGER.name))
        )
        builder.row(types.InlineKeyboardButton(
            text=UserButtons.GET_ARRAY_INVOICES.value,
            callback_data=str(UserButtons.GET_ARRAY_INVOICES.name))
        )
        return builder.as_markup()

    @staticmethod
    def continue_invoice_or_drop():
        """Выбор продолжения/дропа накладной"""
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text=InvoiceButtons.CONTINUE.value,
            callback_data=str(InvoiceButtons.CONTINUE.name))
        )
        builder.row(types.InlineKeyboardButton(
            text=InvoiceButtons.END.value,
            callback_data=str(InvoiceButtons.END.name))
        )
        return builder.as_markup()

    @staticmethod
    def continue_claim_or_drop():
        """Выбор продолжения/дропа претензии"""
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text=InvoiceButtons.CONTINUE.value,
            callback_data=str(ClaimButtons.CONTINUE.name))
        )
        builder.row(types.InlineKeyboardButton(
            text=InvoiceButtons.END.value,
            callback_data=str(ClaimButtons.END.name))
        )
        return builder.as_markup()

    @staticmethod
    def payment_type_buttons():
        """Выбор типа оплаты"""
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text=PaymentType.CASH.value,
            callback_data=str(PaymentType.CASH.name))
        )
        builder.row(types.InlineKeyboardButton(
            text=PaymentType.DC.value,
            callback_data=str(PaymentType.DC.name))
        )
        builder.row(types.InlineKeyboardButton(
            text=PaymentType.SBP.value,
            callback_data=str(PaymentType.SBP.name))
        )
        return builder.as_markup()

    @staticmethod
    def break_invoice():
        """Кнопки для отмены генерации наклданой"""
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text=UserButtons.BREAK_INVOICE.value,
            callback_data=str(UserButtons.BREAK_INVOICE.name))
        )
        return builder.as_markup()

    @staticmethod
    def break_claim():
        """Кнопки для отмены генерации наклданой"""
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text=UserButtons.BREAK_CLAIM.value,
            callback_data=str(UserButtons.BREAK_CLAIM.name))
        )
        return builder.as_markup()

    @staticmethod
    def manager_buttons():
        """Менеджерские кнопки"""
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text=ManagerButtons.GET_USER.value,
            callback_data=str(ManagerButtons.GET_USER.name))
        )
        return builder.as_markup()

    @staticmethod
    def admin_buttons():
        """Админские кнопки"""
        builder = InlineKeyboardBuilder()
        return builder.as_markup()

    @staticmethod
    def superuser_buttons():
        """Кнопки владельца"""
        builder = InlineKeyboardBuilder()
        return builder.as_markup()
