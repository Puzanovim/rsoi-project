from datetime import datetime

from fastapi import APIRouter, Depends, status

from statistic_service.auth import get_superuser
from statistic_service.db.repository import StatisticRepository, get_statistic_repo
from statistic_service.schemas import (
    InputStatistic,
    InputStatisticFields,
    StatisticFilter,
    StatisticModel,
    StatisticPage,
    UserModel,
)

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK, response_model=StatisticPage)
async def get_statistics(
    page: int = 1,
    size: int = 100,
    service: str | None = None,
    start_time: datetime | None = None,
    finish_time: datetime | None = None,
    repo: StatisticRepository = Depends(get_statistic_repo),
    current_user: UserModel = Depends(get_superuser),
) -> StatisticPage:
    statistic_filter: StatisticFilter = StatisticFilter(service=service, start_time=start_time, finish_time=finish_time)
    statistics = await repo.get_statistics(statistic_filter)

    result_count = len(statistics)

    if result_count < size:
        page = 1
        size = result_count
    else:
        lower_bound = (page - 1) * size
        upper_bound = page * size
        statistics = statistics[lower_bound:upper_bound]

    return StatisticPage(page=page, size=size, total_elements=result_count, items=statistics)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=StatisticModel)
async def add_statistic(
    input_statistic_fields: InputStatisticFields,
    repo: StatisticRepository = Depends(get_statistic_repo),
) -> StatisticModel:
    return await repo.add_statistic(InputStatistic(**input_statistic_fields.dict()))
