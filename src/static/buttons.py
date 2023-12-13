"""Текст для кнопок"""

import enum


class UserButtons(enum.Enum):
    """Текст на кнопках для пользователя"""
    CR_INVOICE = "Создать накладную"
    CR_CLAIM = "Создать претензию"
    CALL_MANAGER = "Обратиться в чат поддержки"
    BREAK_INVOICE = "Прекратить создание накладной"
    GET_ARRAY_INVOICES = "Мои накладные"
    BREAK_CLAIM = "Прекратить создание претензии"


class InvoiceButtons(enum.Enum):
    """Текст для кнопок продолжения наклдной"""
    CONTINUE = "Продолжить накладную"
    END = "Удалить незаконченную накладную"


class ClaimButtons(enum.Enum):
    """Текст для кнопок продолжения наклдной"""
    CONTINUE = "Продолжить накладную"
    END = "Удалить незаконченную накладную"


class ManagerButtons(enum.Enum):
    """Текст на кнопках для менеджера"""
    GET_USER = "Информацию о пользователе"
