from typing import List
from uuid import UUID

from pydantic import BaseModel


class UserModel(BaseModel):
    id: UUID
    is_superuser: bool


class InputNamespace(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UpdateNamespace(InputNamespace):
    name: str | None = None  # type: ignore
    owner_id: UUID | None = None  # type: ignore


class NamespaceModel(InputNamespace):
    id: UUID
    owner_id: UUID


class NamespaceModelWithUsers(NamespaceModel):
    users: List[UUID]


class NamespaceUsers(BaseModel):
    users: List[UUID]


class UserNamespaces(BaseModel):
    namespaces: List[UUID]


class UserNamespace(BaseModel):
    user_id: UUID
    namespace_id: UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NamespacePage(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[NamespaceModelWithUsers]


class UserNamespacesPage(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[NamespaceModel]


class StatisticMessage(BaseModel):
    service: str
    description: str
