"""Декларативные модели для БД"""

import datetime
import enum
from typing import Annotated, Optional, List

from sqlalchemy import (
    String,
    Float,
    ForeignKey,
    Integer,
    text,
    ARRAY
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

IntPK = Annotated[int, mapped_column(primary_key=True)]
CreatedAT = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())")
)]
UpdatedAT = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow,
)]


class RoleType(enum.Enum):
    """Уровни доступа"""
    USER = "user"
    MANAGER = "manager"
    ADMIN = "admin"
    SUPERUSER = "superuser"


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    id: Mapped[IntPK]
    telegram_id: Mapped[int] = mapped_column(Integer(), unique=True)
    role: Mapped["RoleType"] = mapped_column(default=RoleType.USER)
    created_at: Mapped[CreatedAT]
    updated_at: Mapped[UpdatedAT]
    is_active: Mapped[bool] = mapped_column(default=True)

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("managers.id", ondelete="SET NULL"),
        nullable=True,
    )
    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="user",
        uselist=True
    )
    manager: Mapped["Manager"] = relationship(
        back_populates="clients"
    )


class Manager(Base):
    """Модель менджера"""
    __tablename__ = "managers"
    id: Mapped[IntPK]
    telegram_id: Mapped[int] = mapped_column(Integer(), unique=True)
    created_at: Mapped[CreatedAT]
    updated_at: Mapped[UpdatedAT]
    clients: Mapped[Optional[List["User"] | None]] = relationship(
        back_populates="manager",
        uselist=True
    )


class PaymentType(enum.Enum):
    """Типы оплаты"""
    CASH = "Cash"
    DC = "DebitCard"


class Invoice(Base):
    """Модель накладной"""
    __tablename__ = "invoices"
    id: Mapped[IntPK]
    description: Mapped[str] = mapped_column(
        String(256)
    )
    weight: Mapped[float] = mapped_column(
        Float(6)
    )
    height: Mapped[int]
    length: Mapped[int]
    width: Mapped[int]
    where_from: Mapped[str]
    to_location: Mapped[str]
    created_at: Mapped[CreatedAT]
    updated_at: Mapped[UpdatedAT]
    payment: Mapped["PaymentType"]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )

    user: Mapped["User"] = relationship(
        back_populates="invoices"
    )


class Claim(Base):
    """Модель претензии"""
    __tablename__ = "claims"
    id: Mapped[IntPK]
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE")
    )
    email: Mapped[str]
    description: Mapped[str]
    required_amount: Mapped[int]
    photos: Mapped[list[str]] = mapped_column(ARRAY(String()), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[CreatedAT]
    updated_at: Mapped[UpdatedAT]
