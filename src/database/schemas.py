"""Schemas"""

from pydantic import BaseModel, ConfigDict


class MyModel(BaseModel):
    """my config"""
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class GetInvoice(MyModel):
    """schema for get Invoice"""
    id: int
    description: str
    weight: float
    height: float
    length: float
    width: float
    where_from: str
    to_location: str
    user_id: int


class InsertInvoice(MyModel):
    """schema for insert Invoice"""
    description: str
    weight: float
    height: float
    length: float
    width: float
    where_from: str
    to_location: str
    user_id: int
    payment: str
