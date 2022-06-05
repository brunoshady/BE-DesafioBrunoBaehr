from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None


class UserPatch(UserCreate):
    name: Union[str, None] = None
    cpf: Union[str, None] = None
    email: Union[str, None] = None
    phone_number: Union[str, None] = None


class User(BaseModel):
    id: int
    name: str
    cpf: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: Union[datetime, None] = None

    class Config:
        orm_mode = True
