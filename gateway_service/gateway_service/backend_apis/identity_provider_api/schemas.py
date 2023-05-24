from typing import List
from uuid import UUID

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    first_name: str
    second_name: str
    email: str
    is_superuser: bool = False


class InputUser(BaseUser):
    password: str


class UpdateUser(InputUser):
    username: str | None = None  # type: ignore
    first_name: str | None = None  # type: ignore
    second_name: str | None = None  # type: ignore
    email: str | None = None  # type: ignore
    password: str | None = None  # type: ignore
    is_superuser: bool | None = None  # type: ignore


class UserModel(BaseUser):
    id: UUID


class UsersPagination(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[UserModel]
