import uuid
from typing import List, Dict

import pytest
from httpx import AsyncClient

from category_service.main import app
from category_service.schemas import CategoryModel, InputCategory
from category_service_tests.conftest import NAMESPACES, CATEGORIES


@pytest.mark.parametrize(
    'page, size, namespace_id',
    [
        (0, 100, NAMESPACES[0]),
        (0, 100, NAMESPACES[1]),
        (0, 100, uuid.uuid4()),
    ],
)
@pytest.mark.asyncio
async def test_get_categories(
    base_url: str, categories: Dict[uuid.UUID, List[CategoryModel]], page: int, size: int, namespace_id: uuid.UUID
) -> None:
    params = {'page': page, 'size': size, 'namespace_id': namespace_id}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get('/categories', params=params)  # type: ignore

    assert response.status_code == 200

    category_page = response.json()

    # assert category_page['page'] == page
    # assert category_page['size'] == size
    # assert len(category_page['items']) == len(categories.get(namespace_id, []))


@pytest.mark.asyncio
async def test_get_category(base_url: str, category: CategoryModel) -> None:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f'/categories/{category.id}')

    assert response.status_code == 200

    gotten_category = response.json()

    assert gotten_category['id'] == category.id
    assert gotten_category['name'] == category.name
    assert gotten_category['namespace_id'] == category.namespace_id


@pytest.mark.asyncio
async def test_get_not_existed_category(base_url: str) -> None:
    category_id = uuid.uuid4()
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f'/categories/{category_id}')

    assert response.status_code == 404


@pytest.mark.parametrize('input_category', CATEGORIES)
@pytest.mark.asyncio
async def test_add_category(base_url: str, input_category: InputCategory) -> None:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post(f'/categories', json=input_category.dict())

    assert response.status_code == 201

    created_category = response.json()
    assert created_category['name'] == input_category.name
    assert created_category['namespace_id'] == input_category.namespace_id


@pytest.mark.asyncio
async def test_delete_category(base_url: str, category: CategoryModel) -> None:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.delete(f'/categories/{category.id}')

    assert response.status_code == 204

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f'/categories/{category.id}')

    assert response.status_code == 404
