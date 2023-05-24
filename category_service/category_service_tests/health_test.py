import pytest
from httpx import AsyncClient

from category_service.main import app


@pytest.mark.asyncio
async def test_health_check(base_url: str) -> None:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get('/manage/health')
    assert response.status_code == 200
    assert response.json() == {'Service': 'Category'}
