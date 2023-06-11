from uuid import UUID

from fastapi import APIRouter, Depends, status

from gateway_service.auth import get_user_token
from gateway_service.backend_apis import CategoryServiceAPI, get_category_service_api
from gateway_service.backend_apis.category_service_api.schemas import CategoryModel, CategoryPagination, InputCategory

router = APIRouter()


@router.get('', status_code=status.HTTP_200_OK, response_model=CategoryPagination)
async def get_categories(
    namespace_id: UUID,
    page: int = 1,
    size: int = 100,
    category_service_api: CategoryServiceAPI = Depends(get_category_service_api),
    access_token: str = Depends(get_user_token),
) -> CategoryPagination:
    return await category_service_api.get_categories(namespace_id, page, size, access_token)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=CategoryModel)
async def create_category(
    input_category: InputCategory,
    category_service_api: CategoryServiceAPI = Depends(get_category_service_api),
    access_token: str = Depends(get_user_token),
) -> CategoryModel:
    return await category_service_api.create_category(input_category, access_token)


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    category_service_api: CategoryServiceAPI = Depends(get_category_service_api),
    access_token: str = Depends(get_user_token),
) -> None:
    await category_service_api.delete_category(category_id, access_token)
