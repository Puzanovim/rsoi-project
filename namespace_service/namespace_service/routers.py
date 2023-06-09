from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from namespace_service.auth import get_current_user, get_superuser
from namespace_service.db.repository import NamespaceRepository, get_namespace_repo
from namespace_service.kafka_producer import KafkaProducer, get_kafka_producer
from namespace_service.schemas import (
    InputNamespace,
    NamespaceModel,
    NamespaceModelWithUsers,
    NamespaceUsers,
    UserModel,
    UserNamespace,
    UserNamespaces,
    UserNamespacesPage,
)

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK, response_model=UserNamespacesPage)
async def get_user_namespaces(
    page: int = 1,
    size: int = 100,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_current_user),
) -> UserNamespacesPage:
    user_namespaces: UserNamespaces = await repo.get_user_namespaces(current_user.id)

    namespaces: List[NamespaceModel] = [
        await repo.get_namespace(namespace_id) for namespace_id in user_namespaces.namespaces
    ]

    result_count = len(user_namespaces.namespaces)

    if result_count < size:
        page = 1
        size = result_count
    else:
        lower_bound = (page - 1) * size
        upper_bound = page * size
        namespaces = namespaces[lower_bound:upper_bound]

    return UserNamespacesPage(page=page, size=size, total_elements=result_count, items=namespaces)


@router.get('/{namespace_id}', status_code=status.HTTP_200_OK, response_model=NamespaceModelWithUsers)
async def get_namespace(
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_current_user),
) -> NamespaceModelWithUsers:
    namespace_model: NamespaceModel = await repo.get_namespace(namespace_id)
    if namespace_model.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only namespace owner can get info about it')
    namespace_users: NamespaceUsers = await repo.get_namespace_users(namespace_model.id)
    return NamespaceModelWithUsers(**namespace_model.dict(), users=namespace_users.users)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=NamespaceModel)
async def create_namespace(
    namespace: InputNamespace,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    kafka: KafkaProducer = Depends(get_kafka_producer),
    current_user: UserModel = Depends(get_current_user),
) -> NamespaceModel:
    namespace = await repo.create_namespace(namespace, current_user.id)
    await repo.add_user_to_namespace(namespace.id, current_user.id)
    await kafka.pull(f'Created namespace: {namespace.name} owner {namespace.owner_id}')
    return namespace


@router.delete('/{namespace_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_namespace(
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    kafka: KafkaProducer = Depends(get_kafka_producer),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    namespace: NamespaceModel = await repo.get_namespace(namespace_id)
    if namespace.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only namespace owner can delete it')
    namespace_users: NamespaceUsers = await repo.get_namespace_users(namespace_id)
    for user_id in namespace_users.users:
        await repo.delete_user_from_namespace(namespace_id, user_id)
    await kafka.pull(f'Deleted namespace {namespace.name}')
    await repo.delete_namespace(namespace_id)


@router.get('/{namespace_id}/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserNamespace)
async def get_user_in_namespace(
    user_id: UUID,
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_current_user),
) -> UserNamespace:
    return await repo.get_namespace_user(user_id, namespace_id)


@router.get('/{namespace_id}/users/me', status_code=status.HTTP_200_OK, response_model=UserNamespace)
async def get_self_user_in_namespace(
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    current_user: UserModel = Depends(get_current_user),
) -> UserNamespace:
    return await repo.get_namespace_user(current_user.id, namespace_id)


@router.post('/{namespace_id}/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def add_user_to_namespace(
    user_id: UUID,
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    kafka: KafkaProducer = Depends(get_kafka_producer),
    current_user: UserModel = Depends(get_superuser),
) -> None:
    namespace: NamespaceModel = await repo.get_namespace(namespace_id)
    if namespace.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Only namespace owner can add new namespace memberships'
        )
    await repo.add_user_to_namespace(namespace_id, user_id)
    await kafka.pull(f'Added {user_id} to namespace {namespace.name}')


@router.delete('/{namespace_id}/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_from_namespace(
    user_id: UUID,
    namespace_id: UUID,
    repo: NamespaceRepository = Depends(get_namespace_repo),
    kafka: KafkaProducer = Depends(get_kafka_producer),
    current_user: UserModel = Depends(get_superuser),
) -> None:
    namespace: NamespaceModel = await repo.get_namespace(namespace_id)
    if namespace.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Only namespace owner can delete namespace memberships'
        )
    if namespace.owner_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Can not delete namespace owner from namespace'
        )
    await repo.delete_user_from_namespace(namespace_id, user_id)
    await kafka.pull(f'Deleted {user_id} to namespace {namespace.name}')
