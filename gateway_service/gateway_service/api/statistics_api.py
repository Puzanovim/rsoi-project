from datetime import datetime

from fastapi import APIRouter, Depends, status

from gateway_service.auth import get_user_token
from gateway_service.backend_apis import StatisticsServiceAPI, get_statistics_service_api
from gateway_service.backend_apis.statistics_service_api.schemas import StatisticFilter, StatisticsPagination

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK, response_model=StatisticsPagination)
async def get_statistics(
    page: int = 1,
    size: int = 100,
    service: str | None = None,
    start_time: datetime | None = None,
    finish_time: datetime | None = None,
    statistics_service_api: StatisticsServiceAPI = Depends(get_statistics_service_api),
    access_token: str = Depends(get_user_token),
) -> StatisticsPagination:
    statistic_filter: StatisticFilter = StatisticFilter(service=service, start_time=start_time, finish_time=finish_time)
    return await statistics_service_api.get_categories(statistic_filter, page, size, access_token)
