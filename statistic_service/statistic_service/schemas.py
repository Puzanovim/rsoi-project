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


class InputStatistic(BaseModel):
    service: str
    description: str
    created_time: datetime


class StatisticModel(InputStatistic):
    id: UUID


class StatisticPage(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[StatisticModel]
