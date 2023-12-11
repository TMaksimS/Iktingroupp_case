from pydantic import BaseModel, ConfigDict


class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class GetInvoice(MyModel):
    id: int
    description: str
    weight: float
    height: float
    length: float
    width: float
    where_from: str
    to_location: str
    user_id: int
