from typing import Awaitable, Dict
from uuid import UUID

from httpx import AsyncClient, Response

from gateway_service.backend_apis.identity_provider_api.schemas import InputUser, UpdateUser, UserModel, UsersPagination
from gateway_service.circuit_breaker import CircuitBreaker
from gateway_service.config import IDENTITY_PROVIDER_CONFIG
from gateway_service.exceptions import ServiceNotAvailableError
from gateway_service.validators import json_dump


class IdentityProviderAPI:
    def __init__(self, host: str = IDENTITY_PROVIDER_CONFIG.host, port: int = IDENTITY_PROVIDER_CONFIG.port) -> None:
        self._host = host
        self._port = port

        self._circuit_breaker: CircuitBreaker = CircuitBreaker(name=self.__class__.__name__)

    async def get_users(self, page: int, size: int, access_token: str) -> UsersPagination:
        params = {'page': page, 'size': size}
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func: Awaitable = client.get(f'http://{self._host}:{self._port}/users', headers=headers, params=params)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return UsersPagination(**response.json())

    async def get_user(self, user_id: UUID, access_token: str) -> UserModel:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.get(f'http://{self._host}:{self._port}/users/{user_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return UserModel(**response.json())

    async def get_me(self, access_token: str) -> UserModel:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.get(f'http://{self._host}:{self._port}/users/me', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return UserModel(**response.json())

    async def create_user(self, user_input: InputUser) -> UserModel:
        body: Dict = json_dump(user_input.dict())

        async with AsyncClient() as client:
            func = client.post(f'http://{self._host}:{self._port}/users', json=body)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return UserModel(**response.json())

    async def delete_user(self, user_id: UUID, access_token: str) -> None:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.delete(f'http://{self._host}:{self._port}/users/{user_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return None

    async def update_user(self, user_id: UUID, user_update: UpdateUser, access_token: str) -> UserModel:
        body: Dict = json_dump(user_update.dict())
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.put(f'http://{self._host}:{self._port}/users/{user_id}', headers=headers, json=body)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return UserModel(**response.json())
