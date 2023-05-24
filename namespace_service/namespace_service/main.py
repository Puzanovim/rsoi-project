from typing import Dict, Annotated
from uuid import UUID

import uvicorn
from fastapi import FastAPI, status, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from jose import jwt, JWTError

from namespace_service.config import DB_CONFIG, AUTH_CONFIG
from namespace_service.db.db_config import run_db_migrations
from namespace_service.exceptions import NotFoundNamespace
from namespace_service.routers import router
from namespace_service.schemas import UserModel

app = FastAPI()
app.include_router(router, tags=['Namespace API'])


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Namespace'}


@app.exception_handler(NotFoundNamespace)
async def not_found_category_handler(request: Request, exc: NotFoundNamespace):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': 'Namespace not found'},
    )


async def auth_header(request: Request) -> str:
    authorization = request.headers.get("Authorization")
    scheme, _, token = authorization.partition(" ")
    return token


async def get_current_user(token: Annotated[str, Depends(auth_header)]) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, AUTH_CONFIG.jwt_key, algorithms=[AUTH_CONFIG.algorithm])
        user_id: UUID | None = UUID(payload.get('sub'))
        is_superuser: bool | None = payload.get('role')

        if user_id is None:
            raise credentials_exception

        user = UserModel(id=user_id, is_superuser=is_superuser)
    except JWTError:
        raise credentials_exception

    return user


async def get_superuser(current_user: Annotated[UserModel, Depends(get_current_user)]) -> UserModel:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


if __name__ == "__main__":
    run_db_migrations(DB_CONFIG.dict(), 'namespace_service/db/migrations/')
    uvicorn.run(app, host="0.0.0.0", port=8050)
