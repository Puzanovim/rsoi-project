from uuid import UUID

from fastapi import APIRouter, Depends, status

from identity_provider.auth import get_current_user, get_superuser
from identity_provider.db.repository import UserRepository, get_user_repo
from identity_provider.schemas import InputUser, TokenData, UpdateUser, UserModel, UsersPage

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK, response_model=UsersPage)
async def get_users(
    page: int = 1,
    size: int = 100,
    repo: UserRepository = Depends(get_user_repo),
    current_user: TokenData = Depends(get_superuser),
) -> UsersPage:
    users = await repo.get_users()

    result_count = len(users)

    if result_count < size:
        page = 1
        size = result_count
    else:
        lower_bound = (page - 1) * size
        upper_bound = page * size
        users = users[lower_bound:upper_bound]

    return UsersPage(page=page, size=size, total_elements=result_count, items=users)


@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_me(
    repo: UserRepository = Depends(get_user_repo),
    current_user: TokenData = Depends(get_current_user),
) -> UserModel:
    return await repo.get_user(current_user.id)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def create_user(
    input_user: InputUser,
    repo: UserRepository = Depends(get_user_repo),
) -> UserModel:
    return await repo.create_user(input_user)


@router.put('/{user_id}', status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def update_user(
    user_id: UUID,
    updated_user: UpdateUser,
    repo: UserRepository = Depends(get_user_repo),
    current_user: TokenData = Depends(get_current_user),
) -> UserModel:
    return await repo.update_user(user_id, updated_user)


@router.delete('/{user_id}', status_code=status.HTTP_201_CREATED)
async def delete_user(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repo),
    current_user: TokenData = Depends(get_superuser),
) -> None:
    return await repo.delete_user(user_id)
