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


class InputNote(InputNoteFields):
    author_id: UUID
    created_date: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UpdateNote(InputNote):
    title: str | None
    text: str | None
    namespace_id: UUID | None


class NoteModel(InputNote):
    id: UUID


class NotesPage(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[NoteModel]
