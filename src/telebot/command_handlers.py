"""Хендлер обработки комманд"""

from aiogram import Router, types
from aiogram.filters.command import Command

from src.database.crud import UserORM
from src.database.models import RoleType
from src.config import LOGER
from src.static.answers import UserAnswer, ManagerAnswer
from src.telebot.buttons_fab import Buttons
from src.telebot.permissions import Permission

router = Router()


@LOGER.catch
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Команда /start, отдает панель пользователя"""
    user = message.from_user.id
    res = await UserORM().insert_user(user)
    if res:
        LOGER.info(f"new user registered id={res}")
    await message.answer(
        UserAnswer.START.value,
        reply_markup=Buttons.user_buttons()
    )


@LOGER.catch
@router.message(Command("id"))
async def cmd_get_my_id(message: types.Message):
    """Команда /id"""
    permission = await Permission(message.from_user.id).check(
        [
            RoleType.USER,
            RoleType.MANAGER,
            RoleType.ADMIN,
            RoleType.SUPERUSER
        ]
    )
    if permission:
        await message.answer(str(message.from_user.id))


@LOGER.catch
@router.message(Command("manager"))
async def cmd_panel_manager(message: types.Message):
    """Команда /manager, отдает панель менеджера"""
    permission = await Permission(message.from_user.id).check(
        [
            RoleType.MANAGER,
            RoleType.ADMIN,
            RoleType.SUPERUSER
        ]
    )
    if permission:
        await message.answer(
            ManagerAnswer.START.value,
            reply_markup=Buttons.manager_buttons()
        )


@LOGER.catch
@router.message(Command("admin"))
async def cmd_panel_admin(message: types.Message):
    """Команда /admin, отдает панель админа"""
    permission = await Permission(message.from_user.id).check(
        [
            RoleType.ADMIN,
            RoleType.SUPERUSER
        ]
    )
    return permission


@LOGER.catch
@router.message(Command("superuser"))
async def cmd_panel_superuser(message: types.Message):
    """Команда /admin, отдает панель владельца"""
    permission = await Permission(message.from_user.id).check(
        [
            RoleType.SUPERUSER
        ]
    )
    return permission
