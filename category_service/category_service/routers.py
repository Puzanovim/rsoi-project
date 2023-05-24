from uuid import UUID

from fastapi import APIRouter, status, Depends

from category_service.db.repository import CategoryRepository, get_category_repo
from category_service.auth import get_current_user
from category_service.schemas import CategoryPage, CategoryModel, InputCategory, UserModel

router = APIRouter()


@router.get('/categories', status_code=status.HTTP_200_OK, response_model=CategoryPage)
async def get_categories(
    namespace_id: UUID,
    page: int = 1,
    size: int = 100,
    repo: CategoryRepository = Depends(get_category_repo),
    current_user: UserModel = Depends(get_current_user),
) -> CategoryPage:
    categories = await repo.get_categories(namespace_id)

    result_count = len(categories)

    if result_count < size:
        page = 1
        size = result_count
    else:
        lower_bound = (page - 1) * size
        upper_bound = page * size
        categories = categories[lower_bound:upper_bound]

    return CategoryPage(page=page, size=size, total_elements=result_count, items=categories)


@router.get('/categories/{category_id}', status_code=status.HTTP_200_OK, response_model=CategoryModel)
async def get_category(
    category_id: UUID,
    repo: CategoryRepository = Depends(get_category_repo),
    current_user: UserModel = Depends(get_current_user),
) -> CategoryModel:
    return await repo.get_category(category_id)


@router.post('/categories', status_code=status.HTTP_201_CREATED, response_model=CategoryModel)
async def create_category(
    category: InputCategory,
    repo: CategoryRepository = Depends(get_category_repo),
    current_user: UserModel = Depends(get_current_user),
) -> CategoryModel:
    return await repo.create_category(category)


@router.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    repo: CategoryRepository = Depends(get_category_repo),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    return await repo.delete_category(category_id)


@router.get('/notes/{note_id}/categories', status_code=status.HTTP_200_OK, response_model=CategoryPage)
async def get_note_categories(
    note_id: UUID,
    page: int = 1,
    size: int = 100,
    repo: CategoryRepository = Depends(get_category_repo),
    current_user: UserModel = Depends(get_current_user),
) -> CategoryPage:
    categories = await repo.get_note_categories(note_id)

    result_count = len(categories)

    if result_count < size:
        page = 1
        size = result_count
    else:
        lower_bound = (page - 1) * size
        upper_bound = page * size
        categories = categories[lower_bound:upper_bound]

    return CategoryPage(page=page, size=size, total_elements=result_count, items=categories)


@router.post('/notes/{note_id}/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def add_category_to_note(
    note_id: UUID,
    category_id: UUID,
    repo: CategoryRepository = Depends(get_category_repo),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    return await repo.add_category_to_note(category_id, note_id)
