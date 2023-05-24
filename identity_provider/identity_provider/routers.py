import uuid
from datetime import timedelta, datetime
from typing import Annotated, Dict, Any

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

from identity_provider.schemas import UserModel, Token, InputUser, TokenData

router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

CODES = {}
CLIENTS = {
    'gateway': 'http://localhost:8080/code'
}

fake_users_db = {
    uuid.UUID('220b393c-9139-4ebe-806c-87f630018844'): {
        'id': uuid.UUID('220b393c-9139-4ebe-806c-87f630018844'),
        "username": "johndoe",
        "first_name": "John Doe",
        "second_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_superuser": False,
    },
    uuid.UUID('9037de2d-03aa-4450-b741-fa96a7be367a'): {
        'id': uuid.UUID('9037de2d-03aa-4450-b741-fa96a7be367a'),
        "username": "admin",
        "first_name": "admin",
        "second_name": "admin",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$JFkoGXGVs5q34PZD8vutqe6j0xsGi9qqB9dnXzj55A2quqkm0JHRW",
        "is_superuser": True,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Dict[uuid.UUID, Dict[str, Any]], user_id: uuid.UUID) -> UserModel | None:
    if user_id in db:
        user_dict = db[user_id]
        return UserModel(**user_dict)


def get_user_by_username(db: Dict[uuid.UUID, Dict[str, Any]], username: str) -> UserModel | None:
    for user in db.values():
        if user['username'] == username:
            return UserModel(**user)
    return None


def authenticate_user(fake_db, username: str, password: str):
    user: UserModel | None = get_user_by_username(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: uuid.UUID = uuid.UUID(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token")
async def login_for_code(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    client_id: str,
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    code = uuid.uuid4()
    CODES[code] = user
    url = CLIENTS.get(client_id, None)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed client",
            headers={"WWW-Authenticate": "Bearer"},
        )
    url += f'?code={code}'
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@router.post("/access_token", response_model=Token)
async def login_for_access_token(
    code: uuid.UUID
):
    if code in CODES:
        user = CODES[code]
        CODES.pop(code)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong code",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': str(user.id), 'is_superuser': user.is_superuser}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserModel)
async def read_users_me(
        current_user: Annotated[UserModel, Depends(get_current_user)]
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
        current_user: Annotated[UserModel, Depends(get_current_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
