from typing import List
from uuid import UUID

from pydantic import BaseModel

from gateway_service.backend_apis.category_service_api.schemas import CategoryModel


class InputNote(BaseModel):
    title: str
    text: str
    namespace_id: UUID


class UpdateNote(InputNote):
    title: str | None  # type: ignore
    text: str | None  # type: ignore
    namespace_id: UUID | None  # type: ignore


class NoteModel(InputNote):
    id: UUID


class FullNote(NoteModel):
    categories: List[CategoryModel] = []


class CreateFullNote(InputNote):
    categories: List[UUID]


class UpdateFullNote(CreateFullNote):
    title: str | None = None  # type: ignore
    text: str | None = None  # type: ignore
    namespace_id: UUID | None = None  # type: ignore
    categories: List[UUID] | None = None  # type: ignore


class NotesPagination(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[NoteModel] = []
