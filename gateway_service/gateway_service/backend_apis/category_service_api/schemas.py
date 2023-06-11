from typing import List
from uuid import UUID

from pydantic import BaseModel


class InputCategory(BaseModel):
    name: str
    namespace_id: UUID


class CategoryModel(InputCategory):
    id: UUID


class CategoryPagination(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[CategoryModel]


class NoteCategories(BaseModel):
    items: List[CategoryModel]
