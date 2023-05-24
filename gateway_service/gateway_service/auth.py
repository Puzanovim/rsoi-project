from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='login', tokenUrl='token')


async def get_user_token(token: str = Depends(oauth2_scheme)) -> str:
    return token
