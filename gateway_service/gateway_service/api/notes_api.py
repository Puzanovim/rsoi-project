from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from gateway_service.auth import get_user_token
from gateway_service.backend_apis import (
    CategoryServiceAPI,
    NamespaceServiceAPI,
    NotesServiceAPI,
    get_category_service_api,
    get_namespace_service_api,
    get_notes_service_api,
)
from gateway_service.backend_apis.category_service_api.schemas import NoteCategories
from gateway_service.backend_apis.notes_service_api.schemas import (
    CreateFullNote,
    FullNote,
    InputNote,
    NoteModel,
    NotesPagination,
    UpdateFullNote,
    UpdateNote,
)
from gateway_service.exceptions import AccessDenied

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK, response_model=NotesPagination)
async def get_notes(
    namespace_id: UUID,
    page: int = 1,
    size: int = 100,
    notes_system_api: NotesServiceAPI = Depends(get_notes_service_api),
    access_token: str = Depends(get_user_token),
) -> NotesPagination:
    return await notes_system_api.get_notes(namespace_id, page, size, access_token)


@router.get('/{note_id}', status_code=status.HTTP_200_OK, response_model=FullNote)
async def get_note(
    note_id: UUID,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    notes_system_api: NotesServiceAPI = Depends(get_notes_service_api),
    category_service_api: CategoryServiceAPI = Depends(get_category_service_api),
    access_token: str = Depends(get_user_token),
) -> FullNote:
    note: NoteModel = await notes_system_api.get_note(note_id, access_token)

    if not await namespace_system_api.check_current_user_in_namespace(note.namespace_id, access_token):
        raise AccessDenied

    categories: NoteCategories | None = await category_service_api.get_note_categories(note_id, access_token)
    return FullNote(**note.dict(), categories=categories.items if categories is not None else [])


@router.post('', status_code=status.HTTP_201_CREATED, response_model=FullNote)
async def create_note(
    new_note: CreateFullNote,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    notes_system_api: NotesServiceAPI = Depends(get_notes_service_api),
    category_service_api: CategoryServiceAPI = Depends(get_category_service_api),
    access_token: str = Depends(get_user_token),
) -> FullNote:
    if not await namespace_system_api.check_current_user_in_namespace(new_note.namespace_id, access_token):
        raise AccessDenied

    created_note = await notes_system_api.create_note(InputNote(**new_note.dict()), access_token)

    for category_id in new_note.categories:
        await category_service_api.add_category_to_note(created_note.id, category_id, access_token)

    categories: NoteCategories | None = await category_service_api.get_note_categories(created_note.id, access_token)
    return FullNote(**created_note.dict(), categories=categories.items if categories is not None else [])


@router.put('/{note_id}', status_code=status.HTTP_201_CREATED, response_model=FullNote)
async def update_note(
    note_id: UUID,
    updated_full_note: UpdateFullNote,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    notes_system_api: NotesServiceAPI = Depends(get_notes_service_api),
    category_service_api: CategoryServiceAPI = Depends(get_category_service_api),
    access_token: str = Depends(get_user_token),
) -> FullNote:
    note: NoteModel = await notes_system_api.get_note(note_id, access_token)

    if not await namespace_system_api.check_current_user_in_namespace(note.namespace_id, access_token):
        raise AccessDenied

    updated_note = await notes_system_api.update_note(UpdateNote(**updated_full_note.dict()), access_token)

    if updated_full_note.categories:
        note_categories: NoteCategories | None = await category_service_api.get_note_categories(note_id, access_token)
        categories: List = note_categories.items if note_categories is not None else []

        for category in categories:
            await category_service_api.delete_category_from_note(note_id, category.id, access_token)

        for category_id in updated_full_note.categories:
            await category_service_api.add_category_to_note(note_id, category_id, access_token)

    note_categories = await category_service_api.get_note_categories(note_id, access_token)
    return FullNote(**updated_note.dict(), categories=note_categories.items if note_categories is not None else [])


@router.delete('/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: UUID,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    notes_system_api: NotesServiceAPI = Depends(get_notes_service_api),
    category_service_api: CategoryServiceAPI = Depends(get_category_service_api),
    access_token: str = Depends(get_user_token),
) -> None:
    note: NoteModel = await notes_system_api.get_note(note_id, access_token)

    if not await namespace_system_api.check_current_user_in_namespace(note.namespace_id, access_token):
        raise AccessDenied

    note_categories: NoteCategories | None = await category_service_api.get_note_categories(note_id, access_token)
    categories: List = note_categories.items if note_categories is not None else []
    for category in categories:
        await category_service_api.delete_category_from_note(note_id, category.id, access_token)

    await notes_system_api.delete_note(note_id, access_token)
