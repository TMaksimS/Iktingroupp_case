"""ORM взаимодествие со всеми моделями из БД"""

from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload

from src.database import async_session_factory
from src.database.models import User, Manager, Invoice, Claim, RoleType
from src.config import LOGER


class UserORM:
    """Обьект инициализации методов для пользователя"""

    def __init__(self):
        self.session = async_session_factory()

    async def insert_user(self, ut_id: int, role: RoleType = None) -> int | None:
        """Метод создает пользователя"""
        async with self.session as session:
            user = User(telegram_id=ut_id)
            if role:
                user.role = role
            session.add(user)
            try:
                await session.flush()
                res = user.id
                await session.commit()
                return res
            except IntegrityError:
                await session.close()
        return None

    async def delete_user(self, telegram_id: int) -> bool | None:
        """Метод удаляет пользователя,
         меняет значение is_active на False,
         фактически пользователь остается в БД"""
        async with self.session as session:
            query = select(User).where(User.telegram_id == telegram_id)
            obj = await session.scalar(query)
            if obj:
                obj.is_active = False
                await session.flush()
                await session.commit()
                return True
        return None

    async def add_manager(self, ut_id: int, manager_id: int):
        """Метод добавляет менеджера к пользователю"""
        async with self.session as session:
            query = select(User).where(User.telegram_id == ut_id)
            obj = await session.scalar(query)
            obj.manager_id = manager_id
            await session.flush()
            await session.commit()

    async def get_user(self, ut_id: int) -> User | None:
        """Метод вызывает пользователя из БД"""
        async with self.session as session:
            query = select(User).where(User.telegram_id == ut_id)
            res = await session.scalar(query)
            return res

    async def get_user_with_invoices(self, ut_id: int) -> User | None:
        """Метод возвращает пользователя со списком его накладных"""
        async with self.session as session:
            query = select(User).where(
                User.telegram_id == ut_id
            ).options(selectinload(User.invoices))
            res = await session.execute(query)
            result = res.scalar()
        return result

    @LOGER.catch
    async def update_user(self, ut_id: int, **kwargs) -> bool | None:
        """Метод обновляет информацию о пользователе"""
        async with self.session as session:
            stmt = update(User).where(User.telegram_id == ut_id).values(kwargs).returning(User)
            obj = await session.execute(stmt)
            if obj.scalar():
                await session.commit()
                return True
            await session.rollback()
            return None


class ManagerORM:
    """Обьект инициализации методов для менеджера"""

    def __init__(self):
        self.session = async_session_factory()

    async def insert_manager(self, mt_id: int) -> int | None:
        """Метод создает менеджера"""
        async with self.session as session:
            manager = Manager(telegram_id=mt_id)
            session.add(manager)
            try:
                await session.flush()
                res = manager.id
                await session.commit()
                return res
            except IntegrityError:
                await session.close()
        return None

    async def get_manager_with_clients(self, manager_id: int) -> Manager | None:
        """Метод возвращает все пользователей
         сопоставленных с указанным менеджером"""
        async with self.session as session:
            query = select(Manager).where(
                Manager.id == manager_id
            ).options(selectinload(Manager.clients))
            res = await session.execute(query)
            result = res.scalar()
        return result

    async def delete_manager(self, manager_id: int):
        """Метод удаляет менеджера и выставляет всем
         подконтрольным пользователям значение manager_id=None"""
        async with self.session as session:
            stmt = delete(Manager).where(Manager.id == manager_id)
            await session.execute(stmt)
            await session.commit()

    async def get_manager(self, manager_id: int) -> Manager | None:
        """Метод возвращает всю информацию о менеджере
         без подгрузки подконтрольных пользователей"""
        async with self.session as session:
            res = await session.get(Manager, manager_id)
        return res


class InvoiceORM:
    """Обьект инициализации методов для накладных"""

    def __init__(self):
        self.session = async_session_factory()

    async def insert_invoice(self, data: dict) -> int | None:
        """Метод создает накладную"""
        async with self.session as session:
            invoice = Invoice(**data)
            session.add(invoice)
            try:
                await session.flush()
                res = invoice.id
                await session.commit()
                return res
            except DBAPIError:
                await session.rollback()
                await session.close()
        return None

    async def get_invoice(self, invoice_id: int) -> Invoice | None:
        """Метод возвращает накладную из БД по ее ID"""
        async with self.session as session:
            invoice = await session.get(Invoice, invoice_id)
        return invoice

    async def edit_invoice(self, invoice_id: int, data: dict) -> bool | None:
        """Метод обновляет накладную"""
        async with self.session as session:
            stmt = update(Invoice).where(
                Invoice.id == invoice_id
            ).values(**data).returning(Invoice)
            obj = await session.execute(stmt)
            if obj.scalar():
                await session.commit()
                return True
            await session.rollback()
            return None

    async def delete_invoice(self, invoice_id: int):
        """Метод удаляет накладную"""
        async with self.session as session:
            stmt = delete(Invoice).where(Invoice.id == invoice_id)
            await session.execute(stmt)
            await session.commit()


class ClaimORM:
    """Обьект инициализации методов для претензий"""

    def __init__(self):
        self.session = async_session_factory()

    async def insert_claim(self, data: dict) -> int | None:
        """Метод создает претензию"""
        async with self.session as session:
            obj = Claim(**data)
            session.add(obj)
            try:
                await session.flush()
                res = obj.id
                await session.commit()
                return res
            except IntegrityError:
                await session.rollback()
                await session.close()
        return None

    async def delete_claim(self, claim_id: int) -> bool | None:
        """Метод удаляет претензию (фактически меняет флаг активности)"""
        async with self.session as session:
            query = select(Claim).where(Claim.id == claim_id)
            obj = await session.scalar(query)
            if obj:
                obj.is_active = False
                await session.flush()
                await session.commit()
                return True
            return None

    async def get_claim(self, claim_id: int) -> Claim | None:
        """Метод возвращает претензию из Бд по ее ID"""
        async with self.session as session:
            res = await session.get(Claim, claim_id)
        return res
