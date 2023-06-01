from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from identity_provider.config import AUTH_CONFIG, CLIENTS, CODES, pwd_context
from identity_provider.db.repository import UserRepository, get_user_repo
from identity_provider.schemas import Token, TokenData, UserDB, UserModel

router = APIRouter()

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='/token', tokenUrl='/access_token')


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


async def get_current_user(token: Annotated[str, Depends(auth_header)]) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, AUTH_CONFIG.secret_key, algorithms=[AUTH_CONFIG.algorithm])
        user_id: UUID | None = UUID(payload.get('sub'))
        is_superuser: bool | None = payload.get('is_superuser')

        if user_id is None or is_superuser is None:
            raise credentials_exception

        user = TokenData(id=user_id, is_superuser=is_superuser)
    except JWTError:
        raise credentials_exception

    return user


async def get_superuser(current_user: Annotated[UserModel, Depends(get_current_user)]) -> UserModel:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, repo: UserRepository) -> UserModel | None:
    user: UserDB = await repo.get_user_by_username(username)

    if not verify_password(password, user.hashed_password):
        return None

    return UserModel(**user.dict())


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AUTH_CONFIG.secret_key, algorithm=AUTH_CONFIG.algorithm)
    return encoded_jwt


@router.post("/token")
async def login_for_code(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    client_id: str,
    repo: UserRepository = Depends(get_user_repo),
) -> RedirectResponse:
    user: UserModel | None = await authenticate_user(form_data.username, form_data.password, repo)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    code = uuid4()
    CODES[code] = user
    url = CLIENTS.get(client_id, None)

    if not url:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed client",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        url += f'?code={code}'

    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.post("/access_token", response_model=Token)
async def login_for_access_token(code: UUID) -> Token:
    if code in CODES:
        user = CODES[code]
        CODES.pop(code)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong code",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=AUTH_CONFIG.access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': str(user.id), 'is_superuser': user.is_superuser}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
