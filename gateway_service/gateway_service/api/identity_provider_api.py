from uuid import UUID

from fastapi import APIRouter, Depends, status

from gateway_service.auth import get_user_token
from gateway_service.backend_apis import IdentityProviderAPI, get_identity_provider_api
from gateway_service.backend_apis.identity_provider_api.schemas import InputUser, UpdateUser, UserModel, UsersPagination

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK, response_model=UsersPagination)
async def get_users(
    page: int = 1,
    size: int = 100,
    identity_provider_api: IdentityProviderAPI = Depends(get_identity_provider_api),
    access_token: str = Depends(get_user_token),
) -> UsersPagination:
    return await identity_provider_api.get_users(page, size, access_token)


@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_me(
    identity_provider_api: IdentityProviderAPI = Depends(get_identity_provider_api),
    access_token: str = Depends(get_user_token),
) -> UserModel:
    return await identity_provider_api.get_me(access_token)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def create_user(
    user_input: InputUser,
    identity_provider_api: IdentityProviderAPI = Depends(get_identity_provider_api),
) -> UserModel:
    return await identity_provider_api.create_user(user_input)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    identity_provider_api: IdentityProviderAPI = Depends(get_identity_provider_api),
    access_token: str = Depends(get_user_token),
) -> None:
    await identity_provider_api.delete_user(user_id, access_token)


@router.put('/{user_id}', status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def update_user(
    user_id: UUID,
    updated_user: UpdateUser,
    identity_provider_api: IdentityProviderAPI = Depends(get_identity_provider_api),
    access_token: str = Depends(get_user_token),
) -> UserModel:
    return await identity_provider_api.update_user(user_id, updated_user, access_token)
