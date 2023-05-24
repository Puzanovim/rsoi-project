from typing import List
from uuid import UUID

from pydantic import BaseModel


class InputNamespace(BaseModel):
    name: str


class NamespaceModel(InputNamespace):
    id: UUID


class NamespacePagination(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[NamespaceModel]
