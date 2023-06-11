from typing import Annotated, Dict
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Request, status
from jose import JWTError, jwt

from namespace_service.config import AUTH_CONFIG, DB_CONFIG
from namespace_service.schemas import UserModel


async def auth_header(request: Request) -> str:
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
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
        is_superuser: bool | None = payload.get('is_superuser')

        if user_id is None or is_superuser is None:
            raise credentials_exception

        user = UserModel(id=user_id, is_superuser=is_superuser)
    except JWTError:
        raise credentials_exception

    return user


async def get_superuser(current_user: Annotated[UserModel, Depends(get_current_user)]) -> UserModel:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
