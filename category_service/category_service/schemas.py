from typing import List
from uuid import UUID

from pydantic import BaseModel


class UserModel(BaseModel):
    id: UUID
    is_superuser: bool


class InputCategory(BaseModel):
    name: str
    namespace_id: UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CategoryModel(InputCategory):
    id: UUID


class CategoryPage(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[CategoryModel]


class NoteCategories(BaseModel):
    items: List[CategoryModel]


class StatisticMessage(BaseModel):
    service: str
    description: str
