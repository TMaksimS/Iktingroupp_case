"""Доступы"""

from src.database.models import RoleType
from src.database.crud import UserORM
from src.config import LOGER


class Permission:
    """Доступы к хендлерам"""
    def __init__(self, ut_id):
        self.id = ut_id

    @LOGER.catch
    async def check(self, role: list[RoleType]) -> bool:
        """Проверка уровня доступа"""
        user = await UserORM().get_user(self.id)
        try:
            if user.role in role:
                return True
        except AttributeError:
            return False

    @LOGER.catch
    async def get_permission(self) -> RoleType:
        """Возврат уровня доступа пользователя"""
        user = await UserORM().get_user(self.id)
        return user.role
