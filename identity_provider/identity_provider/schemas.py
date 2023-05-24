from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID
    is_superuser: bool


class InputUser(BaseModel):
    username: str
    first_name: str
    second_name: str
    email: str
    is_superuser: bool = False


class UserModel(InputUser):
    id: UUID
    hashed_password: str


class UpdateUser(InputUser):
    username: str | None
    first_name: str | None
    second_name: str | None
    email: str | None
    is_superuser: bool | None
    hashed_password: str | None
