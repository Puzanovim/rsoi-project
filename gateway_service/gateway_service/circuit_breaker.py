import asyncio
import enum
import logging
from asyncio import Task
from typing import Awaitable

from httpx import ConnectTimeout, Response

from gateway_service.config import CIRCUIT_BREAKER_CONFIG
from gateway_service.exceptions import NotFoundError, UnauthorizedError

logger = logging.getLogger(__name__)


class CircuitBreakerStatus(enum.Enum):
    CLOSED = 'CLOSED'
    OPEN = 'OPEN'
    HALF_OPEN = 'HALF_OPEN'


class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = CIRCUIT_BREAKER_CONFIG.failure_threshold,
        success_threshold: int = CIRCUIT_BREAKER_CONFIG.success_threshold,
        timeout: int = CIRCUIT_BREAKER_CONFIG.timeout,
    ) -> None:
        self._status: CircuitBreakerStatus = CircuitBreakerStatus.CLOSED
        self.name = name

        self._failure_count: int = 0
        self._success_count: int = 0

        self._failure_threshold: int = failure_threshold
        self._success_threshold: int = success_threshold

        self._timeout: int = timeout
        self._wait_timeout_task: Task | None = None

    async def wait_timeout(self) -> None:
        await asyncio.sleep(self._timeout)
        self._status = CircuitBreakerStatus.HALF_OPEN
        self._success_count = 0

    async def request(self, func: Awaitable) -> Response | None:
        response: Response
        match self._status:
            case CircuitBreakerStatus.CLOSED:
                try:
                    response = await func
                except ConnectTimeout as exc:
                    logger.info(f'ConnectTimeout ERROR: {exc}')
                    self._failure_count += 1
                    if self._failure_count >= self._failure_threshold:
                        self._status = CircuitBreakerStatus.OPEN
                        self._wait_timeout_task = await asyncio.create_task(self.wait_timeout(), name='wait timeout')
                    return None
                except Exception as exc:
                    logger.info(f'SOME ERROR: {exc}')
                    return None

                if 500 <= response.status_code < 600:
                    self._failure_count += 1
                    if self._failure_count >= self._failure_threshold:
                        self._status = CircuitBreakerStatus.OPEN
                        self._wait_timeout_task = await asyncio.create_task(self.wait_timeout(), name='wait timeout')
                    return None

                elif response.status_code == 401:
                    raise UnauthorizedError(details=response.json()["detail"])

                elif response.status_code == 404:
                    logger.error(f'NOT FOUND ERROR: {response.json()}')
                    raise NotFoundError(content=response.json())

                return response

            case CircuitBreakerStatus.OPEN:
                return None

            case CircuitBreakerStatus.HALF_OPEN:
                try:
                    response = await func
                except ConnectTimeout as exc:
                    logger.info(f'ConnectTimeout ERROR: {exc}')
                    self._failure_count += 1
                    if self._failure_count >= self._failure_threshold:
                        self._status = CircuitBreakerStatus.OPEN
                        self._wait_timeout_task = await asyncio.create_task(self.wait_timeout(), name='wait timeout')
                    return None
                except Exception as exc:
                    logger.info(f'SOME ERROR: {exc}')
                    return None

                if 200 <= response.status_code < 300:
                    self._success_count += 1
                    if self._success_count >= self._success_threshold:
                        self._status = CircuitBreakerStatus.CLOSED
                        self._failure_count = 0

                elif 500 <= response.status_code < 600:
                    self._status = CircuitBreakerStatus.OPEN
                    self._wait_timeout_task = await asyncio.create_task(self.wait_timeout(), name='wait timeout')
                    return None

                elif response.status_code == 401:
                    raise UnauthorizedError(details=response.json()["detail"])

                elif response.status_code == 404:
                    raise NotFoundError(content=response.json())

                return response
