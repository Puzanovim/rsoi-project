from typing import Dict, Annotated

import uvicorn
from fastapi import FastAPI, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from httpx import AsyncClient
from fastapi.middleware.cors import CORSMiddleware

from gateway_service.routers import router

app = FastAPI()
app.include_router(router)

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='login', tokenUrl='token')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/login')
async def login_user():
    return RedirectResponse(
        url=f'http://localhost:8030/token?client_id=gateway',
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


@app.get('/code')
async def code_handler(code: str) -> Dict:
    async with AsyncClient(base_url='http://identity_provider:8030') as ac:
        response = await ac.post('/access_token', params={'code': code})
    return response.json()


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Gateway'}


async def get_user_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return token


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
