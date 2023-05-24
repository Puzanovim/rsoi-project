from uuid import UUID

from fastapi import APIRouter, Depends, status

from gateway_service.auth import get_user_token
from gateway_service.backend_apis import NamespaceServiceAPI, get_namespace_service_api
from gateway_service.backend_apis.namespace_service_api.schemas import (
    InputNamespace,
    NamespaceModel,
    NamespacePagination,
    UpdateNamespace,
    NamespaceWithUsers,
)

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK, response_model=NamespacePagination)
async def get_namespaces(
    page: int = 1,
    size: int = 100,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    access_token: str = Depends(get_user_token),
) -> NamespacePagination:
    return await namespace_system_api.get_namespaces(page, size, access_token)


@router.get('/{namespace_id}', status_code=status.HTTP_200_OK)
async def get_namespace(
    namespace_id: UUID,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    access_token: str = Depends(get_user_token),
) -> NamespaceWithUsers:
    return await namespace_system_api.get_namespace(namespace_id, access_token)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_namespace(
    namespace_input: InputNamespace,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    access_token: str = Depends(get_user_token),
) -> NamespaceModel:
    return await namespace_system_api.create_namespace(namespace_input, access_token)


@router.delete('/{namespace_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_namespace(
    namespace_id: UUID,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    access_token: str = Depends(get_user_token),
) -> None:
    await namespace_system_api.delete_namespace(namespace_id, access_token)


@router.post('/{namespace_id}/users/{user_id}', status_code=status.HTTP_201_CREATED)
async def add_user_to_namespace(
    namespace_id: UUID,
    user_id: UUID,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    access_token: str = Depends(get_user_token),
) -> None:
    await namespace_system_api.add_user_to_namespace(user_id, namespace_id, access_token)


@router.delete('/{namespace_id}/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_to_namespace(
    namespace_id: UUID,
    user_id: UUID,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    access_token: str = Depends(get_user_token),
) -> None:
    await namespace_system_api.delete_user_from_namespace(user_id, namespace_id, access_token)


@router.put('/{namespace_id}', status_code=status.HTTP_201_CREATED)
async def update_namespace(
    namespace_id: UUID,
    updated_namespace: UpdateNamespace,
    namespace_system_api: NamespaceServiceAPI = Depends(get_namespace_service_api),
    access_token: str = Depends(get_user_token),
) -> None:
    # TODO update namespace
    pass
