"""Конфигурационный файл телеграм приложения"""

from aiogram import Bot, Dispatcher

from src.database.crud import UserORM
from src.database.models import RoleType
from src.settings import BOT_TOKEN
from src.config import LOGER
from src.telebot.command_handlers import router as cmd_router
from src.telebot.callback_handlers import router as cb_router
from src.telebot.message_handler import router as msg_router


async def create_superuser():
    """Корутинф для автосоздания суперпользователя"""
    await UserORM().insert_user(
        ut_id=477154673,
        role=RoleType.SUPERUSER
    )


@LOGER.catch
async def main():
    """Главная корутина для старта телеграмм бота"""
    await create_superuser()
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(cmd_router)
    dp.include_router(cb_router)
    dp.include_router(msg_router)
    LOGER.info("The bot was turned ON")
    await dp.start_polling(bot)
    LOGER.info("The bot was turned OFF")
