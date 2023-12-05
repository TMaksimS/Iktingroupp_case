"""Тесты для crud операций всех моделей из БД"""

import pytest

from src.database.crud import UserORM, ManagerORM


@pytest.mark.parametrize(
    "ut_id, res",
    [
        (123456, 1),
        (123456, None),
        (555666, 3)
    ]
)
async def test_insert_user(ut_id, res):
    """Тесты создания пользователя"""
    obj = await UserORM().insert_user(ut_id)
    assert obj == res


@pytest.mark.parametrize(
    "ut_id, res",
    [
        (555666, True)
    ]
)
async def test_delete_user(ut_id, res):
    """Тест удаления пользователя"""
    obj = await UserORM().delete_user(ut_id)
    assert obj == res


@pytest.mark.parametrize(
    "ut_id, res, flag",
    [
        (123456, 1, True),
        (555666, 3, False)
    ]
)
async def test_get_user(ut_id, res, flag):
    """Тест получения пользователя"""
    obj = await UserORM().get_user(ut_id)
    assert obj.id == res
    assert obj.is_active == flag


@pytest.mark.parametrize(
    "mt_id, res",
    [
        (789456, 1),
        (789456, None),
        (123568, 3)
    ]
)
async def test_insert_manager(mt_id, res):
    """Тест создания менеджера"""
    obj = await ManagerORM().insert_manager(mt_id)
    assert obj == res


@pytest.mark.parametrize(
    "ut_id, manager_id",
    [
        (123456, 1),
        (555666, 1)
    ]
)
async def test_add_manager(ut_id, manager_id):
    """Тест добавления менеджера к пользователю"""
    await UserORM().add_manager(ut_id, manager_id)
    obj = await UserORM().get_user(ut_id)
    assert obj.manager_id == manager_id


@pytest.mark.parametrize(
    "ut_id1, ut_id2, manager_id",
    [
        (123456, 555666, 1)
    ]
)
async def test_manager_get_clients(manager_id, ut_id1, ut_id2):
    """Тест получения всех пользователей приписанных к менеджеру"""
    obj = await ManagerORM().get_clients(manager_id)
    assert obj.clients[0].telegram_id == ut_id1
    assert obj.clients[1].telegram_id == ut_id2


@pytest.mark.parametrize(
    "manager_id, ut_id, res",
    [
        (1, 123456, None)
    ]
)
async def test_delete_manager(manager_id, ut_id, res):
    """Тест удаления пользователя из БД
    и присвоения пустого значения для manager_id в User"""
    await ManagerORM().delete_manager(manager_id)
    user = await UserORM().get_user(ut_id)
    manager = await ManagerORM().get_manager(manager_id)
    assert user.manager_id == res
    assert manager == res
