from typing import Awaitable, Dict
from uuid import UUID

from gateway_service.backend_apis.namespace_service_api.schemas import NamespacePagination, NamespaceModel, InputNamespace
from gateway_service.circuit_breaker import CircuitBreaker
from gateway_service.config import NAMESPACE_SERVICE_CONFIG
from gateway_service.exceptions import ServiceNotAvailableError
from gateway_service.validators import json_dump
from httpx import AsyncClient, Response


class NamespaceServiceAPI:
    def __init__(self, host: str = NAMESPACE_SERVICE_CONFIG.host, port: int = NAMESPACE_SERVICE_CONFIG.port) -> None:
        self._host = host
        self._port = port

        self._circuit_breaker: CircuitBreaker = CircuitBreaker(name=self.__class__.__name__)

    async def get_namespaces(self, page: int, size: int, access_token: str) -> NamespacePagination | None:
        params = {'page': page, 'size': size}
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func: Awaitable = client.get(f'http://{self._host}:{self._port}/namespaces', headers=headers, params=params)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is not None:
            return NamespacePagination(**response.json())

        return None

    async def get_namespace(self, namespace_id: UUID, access_token: str) -> NamespaceModel:
        namespace: NamespaceModel
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.get(f'http://{self._host}:{self._port}/namespaces/{namespace_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is not None:
            namespace = NamespaceModel(**response.json())
        else:
            namespace = NamespaceModel(id=namespace_id, name='')

        return namespace

    async def create_namespace(self, namespace_input: InputNamespace, access_token: str) -> NamespaceModel:
        body: Dict = json_dump(namespace_input.dict())
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.post(f'http://{self._host}:{self._port}/namespaces', headers=headers, json=body)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return NamespaceModel(**response.json())

    async def delete_namespace(self, namespace_id: UUID, access_token: str) -> None:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.delete(f'http://{self._host}:{self._port}/namespaces/{namespace_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return None

    async def check_user_in_namespace(self, namespace_id: UUID, access_token: str) -> bool:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.get(f'http://{self._host}:{self._port}/namespaces/{namespace_id}/users/me', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        return False if response is None else True

    async def add_user_to_namespace(self, user_id: UUID, namespace_id: UUID, access_token: str) -> None:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.post(f'http://{self._host}:{self._port}/namespaces/{namespace_id}/users/{user_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return None

    async def delete_user_from_namespace(self, user_id: UUID, namespace_id: UUID, access_token: str) -> None:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.delete(f'http://{self._host}:{self._port}/namespaces/{namespace_id}/users/{user_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return None
