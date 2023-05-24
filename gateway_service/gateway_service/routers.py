from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2AuthorizationCodeBearer

from gateway_service.backend_apis import NotesServiceAPI, NamespaceServiceAPI, CategoryServiceAPI, get_notes_service_api, get_category_service_api, get_namespace_service_api
from gateway_service.backend_apis.category_service_api.schemas import CategoryPagination
from gateway_service.backend_apis.namespace_service_api.schemas import NamespacePagination
from gateway_service.backend_apis.notes_service_api.schemas import InputNote, NotesPagination, NoteModel
from gateway_service.schemas import CreateFullNote

router = APIRouter()

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='login', tokenUrl='token')


async def get_user_token(token: str = Depends(oauth2_scheme)):
    return token


@router.get('/namespaces', status_code=status.HTTP_200_OK, response_model=NamespacePagination)
async def get_namespaces(
    page: int = 0,
    size: int = 100,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    access_token: str = Depends(get_user_token),
) -> NamespacePagination:
    return await namespace_system_api.get_namespaces(page, size, access_token)


@router.get('/notes', status_code=status.HTTP_200_OK, response_model=NotesPagination)
async def get_notes(
    namespace_id: UUID,
    page: int = 0,
    size: int = 100,
    notes_system_api: NotesServiceAPI = Depends(get_notes_service_api),
    access_token: str = Depends(get_user_token),
) -> NotesPagination:
    return await notes_system_api.get_notes(namespace_id, page, size, access_token)


@router.get('/notes/{note_id}', status_code=status.HTTP_200_OK, response_model=NoteModel)
async def get_notes(
    note_id: UUID,
    notes_system_api: NotesServiceAPI = Depends(get_notes_service_api),
    access_token: str = Depends(get_user_token),
) -> NoteModel:
    return await notes_system_api.get_note(note_id, access_token)


@router.get('/categories', status_code=status.HTTP_200_OK, response_model=CategoryPagination)
async def get_categories(
    namespace_id: UUID,
    page: int = 0,
    size: int = 100,
    category_service_api: CategoryServiceAPI = Depends(get_category_service_api),
    access_token: str = Depends(get_user_token),
) -> CategoryPagination:
    return await category_service_api.get_categories(namespace_id, page, size, access_token)


@router.post('/notes', status_code=status.HTTP_201_CREATED, response_model=NoteModel)
async def create_note(
    new_note: CreateFullNote,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    notes_system_api: NotesServiceAPI = Depends(get_notes_service_api),
    category_service_api: CategoryServiceAPI = Depends(get_category_service_api),
    access_token: str = Depends(get_user_token),
) -> NoteModel:  # TODO note with categories
    await namespace_system_api.check_user_in_namespace(new_note.namespace_id, access_token)
    created_note = await notes_system_api.create_note(InputNote(**new_note.dict()), access_token)
    for category_id in new_note.categories:
        await category_service_api.add_category_to_note(created_note.id, category_id, access_token)

    return created_note
