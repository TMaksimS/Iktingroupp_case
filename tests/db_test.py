"""Тесты для crud операций всех моделей из БД"""

import pytest

from src.database.crud import (
    UserORM,
    ManagerORM,
    InvoiceORM,
    ClaimORM
)


@pytest.mark.parametrize(
    "ut_id, res",
    [
        (123456, 1),
        (123456, None),
        (555666, 3),
        (777888, 4)
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
    obj = await ManagerORM().get_manager_with_clients(manager_id)
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


@pytest.mark.parametrize(
    "data, invoice_id",
    [
        ({
             "description": "test invoice",
             "weight": 15.6,
             "height": 10,
             "length": 5,
             "width": 10,
             "where_from": "Russia, Saratov",
             "to_location": "Russia, Rostov",
             "payment": "CASH",
             "user_id": 1
         }, 1),
        ({
             "description": "test invoice",
             "weight": 15.6,
             "height": 10,
             "length": 5,
             "width": 10,
             "where_from": "Russia, Saratov",
             "to_location": "Russia, Rostov",
             "payment": "cash",
             "user_id": 1
         }, None),
        ({
             "description": "test invoice",
             "weight": 16,
             "height": 10,
             "length": 5,
             "width": 10,
             "where_from": "Russia, Saratov",
             "to_location": "Russia, Rostov",
             "payment": "DC",
             "user_id": 4
         }, 2)
    ]
)
async def test_insert_invoice(data, invoice_id):
    """Тест создания новой накладной"""
    res = await InvoiceORM().insert_invoice(data)
    assert res == invoice_id


@pytest.mark.parametrize(
    "invoice_id, res",
    [
        (1, "Russia, Rostov"),
        (2, "Russia, Rostov"),
        (3, None)
    ]
)
async def test_get_invoice(invoice_id, res):
    """Тест получения данных из накладной"""
    invoice = await InvoiceORM().get_invoice(invoice_id)
    if invoice:
        assert invoice.to_location == res
    else:
        assert invoice == res


@pytest.mark.parametrize(
    "invoice_id, data, res",
    [
        (1, {"weight": 16}, True),
        (2, {"weight": 17}, True),
        (3, {"weight": 18}, None)
    ]
)
async def test_edit_invoice(invoice_id, data, res):
    """Тест обновления данных в накладной"""
    upd_invoice = await InvoiceORM().edit_invoice(invoice_id, data)
    assert upd_invoice == res


@pytest.mark.parametrize(
    "ut_id, count",
    [
        (123456, 1),
        (555666, 0)
    ]
)
async def test_get_user_with_invoices(ut_id, count):
    """Тест проверки количества закрепленных накладных у пользователя"""
    res = await UserORM().get_user_with_invoices(ut_id)
    assert len(res.invoices) == count


@pytest.mark.parametrize(
    "res, ut_id",
    [
        (0, 123456),
    ]
)
async def test_delete_invoice(res, ut_id):
    """Тест удаление накладной"""
    await InvoiceORM().delete_invoice(1)
    user = await UserORM().get_user_with_invoices(ut_id)
    assert len(user.invoices) == res


@pytest.mark.parametrize(
    "data, claim_id",
    [
        ({
             "invoice_id": 2,
             "email": "Example2023@gmail.com",
             "description": "Test claim",
             "required_amount": 5000,
             "photos": ["url1", "url2"]
         }, 1),
        ({
             "invoice_id": 56,
             "email": "Example2023@gmail.com",
             "description": "Test claim",
             "required_amount": 5000,
             "photos": ["url1", "url2"]}, None)

    ]
)
async def test_insert_claim(data, claim_id):
    """Тест проверки создания претензии"""
    res = await ClaimORM().insert_claim(data)
    assert res == claim_id


@pytest.mark.parametrize(
    "claim_id, res",
    [
        (1, True),
        (2, None)
    ]
)
async def test_delete_claim(claim_id, res):
    """Тест удаления претензии"""
    result = await ClaimORM().delete_claim(claim_id)
    assert result == res

@pytest.mark.parametrize(
    "claim_id, res",
    [
        (1, "Example2023@gmail.com"),
        (2, None)
    ]
)
async def test_get_claim(claim_id, res):
    """Тест получения данных из претензии"""
    obj = await ClaimORM().get_claim(claim_id)
    if obj:
        assert obj.email == res
    else:
        assert obj == res
