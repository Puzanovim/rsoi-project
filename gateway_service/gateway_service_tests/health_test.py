import pytest
from httpx import AsyncClient

from gateway_service.main import app


@pytest.mark.asyncio
async def test_health_check() -> None:
    async with AsyncClient(app=app, base_url="http://gateway_service:8080") as ac:
        response = await ac.get("/manage/health")
    assert response.status_code == 200
    assert response.json() == {'Service': 'Gateway'}
