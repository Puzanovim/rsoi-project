from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class StatisticFilter(BaseModel):
    service: str | None = None
    start_time: datetime | None = None
    finish_time: datetime | None = None


class StatisticModel(BaseModel):
    service: str
    description: str
    created_time: datetime
    id: UUID


class StatisticsPagination(BaseModel):
    page: int
    size: int
    total_elements: int
    items: List[StatisticModel]
