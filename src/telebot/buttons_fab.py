"""Кнопочная фабрика"""

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.static.buttons import UserButtons, ManagerButtons


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
            callback_data="Create Claim")
        )
        builder.row(types.InlineKeyboardButton(
            text=UserButtons.CALL_MANAGER.value,
            callback_data="Call Manager")
        )
        builder.row(types.InlineKeyboardButton(
            text=UserButtons.GET_ARRAY_INVOICES.value,
            callback_data=str(UserButtons.GET_ARRAY_INVOICES.name))
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
