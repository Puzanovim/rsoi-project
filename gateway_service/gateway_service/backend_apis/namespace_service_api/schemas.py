from typing import List
from uuid import UUID

from pydantic import BaseModel


class InputNamespace(BaseModel):
    name: str


class UpdateNamespace(InputNamespace):
    name: str | None = None  # type: ignore


class NamespaceModel(InputNamespace):
    id: UUID


class NamespaceWithUsers(NamespaceModel):
    users: List[UUID]


class NamespacePagination(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[NamespaceModel]
