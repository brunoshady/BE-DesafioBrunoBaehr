from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: Optional[int] = None
    item_description:  Optional[str] = None
    item_quantity: Optional[int] = None
    item_price: Optional[float] = None


class OrderPatch(OrderCreate):
    user_id: Union[int, None] = None
    item_description: Union[str, None] = None
    item_quantity: Union[int, None] = None
    item_price: Union[float, None] = None


class Order(BaseModel):
    id: int
    user_id: int
    item_description: str
    item_quantity: int
    item_price: float
    total_value: float
    created_at: datetime
    updated_at: Union[datetime, None] = None

    class Config:
        orm_mode = True
