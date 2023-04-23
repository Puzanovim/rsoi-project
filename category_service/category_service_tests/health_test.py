import pytest
from httpx import AsyncClient

from category_service.main import app


@pytest.mark.asyncio
async def test_health_check() -> None:
    async with AsyncClient(app=app, base_url="http://category_service:8060") as ac:
        response = await ac.get("/manage/health")
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}
