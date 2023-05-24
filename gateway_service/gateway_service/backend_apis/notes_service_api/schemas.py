from typing import List
from uuid import UUID

from pydantic import BaseModel


class InputNote(BaseModel):
    title: str
    text: str
    namespace_id: UUID


class NoteModel(InputNote):
    id: UUID


class NotesPagination(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[NoteModel]
