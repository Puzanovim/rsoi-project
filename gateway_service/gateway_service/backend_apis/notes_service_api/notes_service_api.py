from typing import Awaitable, Dict
from uuid import UUID

from httpx import AsyncClient, Response

from gateway_service.backend_apis.notes_service_api.schemas import InputNote, NoteModel, NotesPagination, UpdateNote
from gateway_service.circuit_breaker import CircuitBreaker
from gateway_service.config import NOTES_SERVICE_CONFIG
from gateway_service.exceptions import ServiceNotAvailableError
from gateway_service.validators import json_dump


class NotesServiceAPI:
    def __init__(self, host: str = NOTES_SERVICE_CONFIG.host, port: int = NOTES_SERVICE_CONFIG.port) -> None:
        self._host = host
        self._port = port

        self._circuit_breaker: CircuitBreaker = CircuitBreaker(name=self.__class__.__name__)

    async def get_notes(self, namespace_id: UUID, page: int, size: int, access_token: str) -> NotesPagination:
        params = {'namespace_id': namespace_id, 'page': page, 'size': size}
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func: Awaitable = client.get(f'http://{self._host}:{self._port}/notes', headers=headers, params=params)  # type: ignore
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return NotesPagination(**response.json())

    async def get_note(self, note_id: UUID, access_token: str) -> NoteModel:
        note: NoteModel
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.get(f'http://{self._host}:{self._port}/notes/{note_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return NoteModel(**response.json())

    async def create_note(self, note_input: InputNote, access_token: str) -> NoteModel:
        body: Dict = json_dump(note_input.dict())
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.post(f'http://{self._host}:{self._port}/notes', headers=headers, json=body)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return NoteModel(**response.json())

    async def update_note(self, note_update: UpdateNote, access_token: str) -> NoteModel:
        body: Dict = json_dump(note_update.dict())
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.put(f'http://{self._host}:{self._port}/notes', headers=headers, json=body)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return NoteModel(**response.json())

    async def delete_note(self, note_id: UUID, access_token: str) -> None:
        headers = {'Authorization': f'Bearer {access_token}'}

        async with AsyncClient() as client:
            func = client.delete(f'http://{self._host}:{self._port}/notes/{note_id}', headers=headers)
            response: Response | None = await self._circuit_breaker.request(func)

        if response is None:
            raise ServiceNotAvailableError

        return None
