from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class UserModel(BaseModel):
    id: UUID
    is_superuser: bool


class StatisticFilter(BaseModel):
    service: str | None = None
    start_time: datetime | None = None
    finish_time: datetime | None = None


class InputStatisticFields(BaseModel):
    service: str
    description: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class InputStatistic(InputStatisticFields):
    created_time: datetime = datetime.utcnow()


class StatisticModel(InputStatistic):
    id: UUID


class StatisticPage(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[StatisticModel]
