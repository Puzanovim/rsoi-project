from typing import Awaitable, Dict
from uuid import UUID

from gateway_service.backend_apis.category_service_api.schemas import CategoryPagination, CategoryModel, InputCategory
from gateway_service.circuit_breaker import CircuitBreaker
from gateway_service.config import CATEGORY_SERVICE_CONFIG
from gateway_service.exceptions import ServiceNotAvailableError
from gateway_service.validators import json_dump
from httpx import AsyncClient, Response


class CategoryServiceAPI:
    def __init__(self, host: str = CATEGORY_SERVICE_CONFIG.host, port: int = CATEGORY_SERVICE_CONFIG.port) -> None:
        self._host = host
        self._port = port

        self._circuit_breaker: CircuitBreaker = CircuitBreaker(name=self.__class__.__name__)

    async def get_categories(self, namespace_id: UUID, page: int, size: int, access_token: str) -> CategoryPagination | None:
        params = {'namespace_id': namespace_id, 'page': page, 'size': size}
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func: Awaitable = client.get(f'http://{self._host}:{self._port}/categories', headers=headers, params=params)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is not None:
            return CategoryPagination(**response.json())

        return None

    async def get_category(self, category_id: UUID, access_token: str) -> CategoryModel:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.get(f'http://{self._host}:{self._port}/categories/{category_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return CategoryModel(**response.json())

    async def create_category(self, category_input: InputCategory, access_token: str) -> CategoryModel:
        body: Dict = json_dump(category_input.dict())
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.post(f'http://{self._host}:{self._port}/categories', headers=headers, json=body)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return CategoryModel(**response.json())

    async def delete_category(self, category_id: UUID, access_token: str) -> None:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.delete(f'http://{self._host}:{self._port}/categories/{category_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return None

    async def get_note_categories(self, note_id: UUID, page: int, size: int, access_token: str) -> CategoryPagination | None:
        params = {'page': page, 'size': size}
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func: Awaitable = client.get(f'http://{self._host}:{self._port}/notes/{note_id}/categories', headers=headers, params=params)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is not None:
            return CategoryPagination(**response.json())

        return None

    async def add_category_to_note(self, note_id: UUID, category_id: UUID, access_token: str) -> CategoryModel:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.post(f'http://{self._host}:{self._port}/notes/{note_id}/categories/{category_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return None

    async def delete_category_from_note(self, note_id: UUID, category_id: UUID, access_token: str) -> None:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.delete(f'http://{self._host}:{self._port}/notes/{note_id}/categories/{category_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return None
