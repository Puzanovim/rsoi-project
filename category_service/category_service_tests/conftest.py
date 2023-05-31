import uuid
from typing import AsyncGenerator, Dict, List

import pytest
import pytest_asyncio
from httpx import AsyncClient

from category_service.main import app
from category_service.schemas import CategoryModel, InputCategory

NAMESPACE_F = uuid.uuid4()
NAMESPACE_S = uuid.uuid4()
NAMESPACES = [NAMESPACE_F, NAMESPACE_S]
CATEGORIES = [
    InputCategory(name='books', namespace_id=NAMESPACE_F),
    InputCategory(name='movies', namespace_id=NAMESPACE_F),
    InputCategory(name='articles', namespace_id=NAMESPACE_S),
]


@pytest.fixture
def category_service_api() -> str:
    return 'category_service'


@pytest.fixture
def category_service_port() -> int:
    return 8060


@pytest.fixture
def base_url(category_service_api: str, category_service_port: int) -> str:
    return f'http://{category_service_api}:{category_service_port}'


@pytest_asyncio.fixture
async def category(base_url: str) -> AsyncGenerator:
    input_category = CATEGORIES[0]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post(f'/categories', json=input_category.dict())

    created_category = CategoryModel(**response.json())
    yield created_category

    async with AsyncClient(app=app, base_url=base_url) as ac:
        await ac.delete(f'/categories/{created_category.id}')


@pytest_asyncio.fixture
async def categories(base_url: str) -> AsyncGenerator:
    created_categories: Dict[uuid.UUID, List[CategoryModel]] = {}
    for namespace in NAMESPACES:
        created_categories[namespace] = []

    for input_category in CATEGORIES:
        async with AsyncClient(app=app, base_url=base_url) as ac:
            response = await ac.post(f'/categories', json=input_category.dict())

        created_category = CategoryModel(**response.json())
        created_categories[created_category.namespace_id].append(created_category)

    yield created_categories

    for namespace in NAMESPACES:
        for created_category in created_categories[namespace]:
            async with AsyncClient(app=app, base_url=base_url) as ac:
                await ac.delete(f'/categories/{created_category.id}')
