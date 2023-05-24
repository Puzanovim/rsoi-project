from typing import List
from uuid import UUID

from pydantic import BaseModel


class CreateFullNote(BaseModel):
    title: str
    text: str
    namespace_id: UUID
    categories: List[UUID]
