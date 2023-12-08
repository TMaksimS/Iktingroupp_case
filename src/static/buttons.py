"""Текст для кнопок"""

import enum


class UserButtons(enum.Enum):
    """Текст на кнопках для пользователя"""
    CR_INVOICE = "Создать накладную"
    CR_CLAIM = "Создать претензию"
    CALL_MANAGER = "Обратиться в чат поддержки"
    BREAK_INVOICE = "Прекратить создание накладной"


class ManagerButtons(enum.Enum):
    """Текст на кнопках для менеджера"""
    GET_USER = "Информацию о пользователе"
