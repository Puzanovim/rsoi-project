from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Depends

from namespace_service.db.repository import NamespaceRepository, get_namespace_repo
from namespace_service.auth import get_current_user, get_superuser
from namespace_service.schemas import NamespaceModel, InputNamespace, \
    UserNamespacesPage, NamespaceModelWithUsers, NamespaceUsers, UserNamespaces, UserModel, UserNamespace

router = APIRouter()


@router.get('/namespaces', status_code=status.HTTP_200_OK, response_model=UserNamespacesPage)
async def get_user_namespaces(
    page: int = 1,
    size: int = 100,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_current_user),
) -> UserNamespacesPage:
    user_namespaces: UserNamespaces = await repo.get_user_namespaces(current_user.id)

    namespaces: List[NamespaceModel] = [await repo.get_namespace(namespace_id) for namespace_id in user_namespaces.namespaces]

    result_count = len(user_namespaces.namespaces)

    if result_count < size:
        page = 1
        size = result_count
    else:
        lower_bound = (page - 1) * size
        upper_bound = page * size
        namespaces = namespaces[lower_bound:upper_bound]

    return UserNamespacesPage(page=page, size=size, total_elements=result_count, items=namespaces)


@router.get('/namespaces/{namespace_id}', status_code=status.HTTP_200_OK, response_model=NamespaceModelWithUsers)
async def get_namespace(
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_current_user),
) -> NamespaceModelWithUsers:
    namespace_model: NamespaceModel = await repo.get_namespace(namespace_id)
    namespace_users: NamespaceUsers = await repo.get_namespace_users(namespace_model.id)
    return NamespaceModelWithUsers(**namespace_model.dict(), users=namespace_users.users)


@router.post('/namespaces', status_code=status.HTTP_201_CREATED, response_model=NamespaceModel)
async def create_namespace(
    namespace: InputNamespace,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_superuser),
) -> NamespaceModel:
    return await repo.create_namespace(namespace)


@router.delete('/namespaces/{namespace_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_namespace(
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_superuser),
) -> None:
    await repo.delete_namespace(namespace_id)


@router.get(
    'namespaces/{namespace_id}/users/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserNamespace
)
async def get_user_in_namespace(
    user_id: UUID,
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_current_user),
) -> UserNamespace:
    return await repo.get_namespace_user(user_id, namespace_id)


@router.get(
    'namespaces/{namespace_id}/users/me',
    status_code=status.HTTP_200_OK,
    response_model=UserNamespace
)
async def get_self_user_in_namespace(
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_current_user),
) -> UserNamespace:
    return await repo.get_namespace_user(current_user.id, namespace_id)


@router.post(
    'namespaces/{namespace_id}/users/{user_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=UserNamespacesPage
)
async def add_user_to_namespace(
    user_id: UUID,
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_superuser),
) -> None:
    await repo.add_user_to_namespace(namespace_id, user_id)


@router.delete(
    '/namespaces/{namespace_id}/users/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_user_from_namespace(
    user_id: UUID,
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_superuser),
) -> None:
    await repo.delete_user_from_namespace(namespace_id, user_id)
