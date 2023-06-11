from typing import List
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID
    is_superuser: bool


class BaseUser(BaseModel):
    username: str
    first_name: str
    second_name: str
    email: str
    is_superuser: bool = False

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class InputUser(BaseUser):
    password: str


class UserModel(BaseUser):
    id: UUID


class UserDB(UserModel):
    hashed_password: str


class UpdateUser(InputUser):
    username: str | None = None  # type: ignore
    first_name: str | None = None  # type: ignore
    second_name: str | None = None  # type: ignore
    email: str | None = None  # type: ignore
    is_superuser: bool | None = None  # type: ignore
    hashed_password: str | None = None  # type: ignore


class UsersPage(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[UserModel]


class StatisticMessage(BaseModel):
    service: str
    description: str
