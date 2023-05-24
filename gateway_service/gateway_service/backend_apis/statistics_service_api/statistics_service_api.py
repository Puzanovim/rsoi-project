from typing import Awaitable

from httpx import AsyncClient, Response

from gateway_service.backend_apis.statistics_service_api.schemas import StatisticFilter, StatisticsPagination
from gateway_service.circuit_breaker import CircuitBreaker
from gateway_service.config import STATISTIC_SERVICE_CONFIG
from gateway_service.exceptions import ServiceNotAvailableError


class StatisticsServiceAPI:
    def __init__(self, host: str = STATISTIC_SERVICE_CONFIG.host, port: int = STATISTIC_SERVICE_CONFIG.port) -> None:
        self._host = host
        self._port = port

        self._circuit_breaker: CircuitBreaker = CircuitBreaker(name=self.__class__.__name__)

    async def get_categories(
        self, statistics_filter: StatisticFilter, page: int, size: int, access_token: str
    ) -> StatisticsPagination:
        params = {'page': page, 'size': size, **statistics_filter.dict(exclude_none=True)}
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func: Awaitable = client.get(f'http://{self._host}:{self._port}/statistics', headers=headers, params=params)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return StatisticsPagination(**response.json())
