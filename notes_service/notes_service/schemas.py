from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class UserModel(BaseModel):
    id: UUID
    is_superuser: bool


class InputNoteFields(BaseModel):
    title: str
    text: str
    namespace_id: UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class InputNote(InputNoteFields):
    author_id: UUID
    created_date: datetime = datetime.utcnow()


class UpdateNote(InputNote):
    title: str | None = None  # type: ignore
    text: str | None = None  # type: ignore
    namespace_id: UUID | None = None  # type: ignore


class NoteModel(InputNote):
    id: UUID


class NotesPage(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[NoteModel]


class StatisticMessage(BaseModel):
    service: str
    description: str
