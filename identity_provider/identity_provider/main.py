import uuid
from typing import Dict

import uvicorn
from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from identity_provider.auth import router as auth_router
from identity_provider.config import ADMIN_CREDS, DB_CONFIG
from identity_provider.db.db_config import run_db_migrations
from identity_provider.db.repository import UserRepository, get_user_repo
from identity_provider.exceptions import NotFoundUser
from identity_provider.routers import router as users_router
from identity_provider.schemas import InputUser

app = FastAPI()
app.include_router(auth_router, tags=['Identity Provider Auth API'])
app.include_router(users_router, prefix='/users', tags=['Identity Provider API'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def app_startup() -> None:
    admin = InputUser(
        **ADMIN_CREDS.dict(),
        is_superuser=True,
    )
    repo: UserRepository = get_user_repo()
    await repo.create_user(admin)


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Identity Provider'}


@app.exception_handler(NotFoundUser)
async def not_found_user_handler(request: Request, exc: NotFoundUser) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': 'User not found'},
    )


if __name__ == "__main__":
    run_db_migrations(DB_CONFIG.dict(), 'identity_provider/db/migrations/')
    uvicorn.run(app, host="0.0.0.0", port=8030)
