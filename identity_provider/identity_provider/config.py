from typing import Dict
from uuid import UUID

from passlib.context import CryptContext
from pydantic import BaseSettings, Field

from identity_provider.schemas import UserModel

CODES: Dict[UUID, UserModel] = {}
CLIENTS = {'gateway': 'http://localhost:8080/code'}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class DBConfig(BaseSettings):
    db_user: str = Field(default='program', allow_mutation=False, env='DB_USER')
    db_password: str = Field(default='test', allow_mutation=False, env='DB_PASS')
    db_host: str = Field(default='postgres', allow_mutation=False, env='DB_HOST')
    db_port: int = Field(default=5432, allow_mutation=False, env='DB_PORT')
    db_name: str = Field(default='users', allow_mutation=False, env='DB_NAME')

    class Config:
        validate_assignment = True


class AuthConfig(BaseSettings):
    secret_key: str = Field(
        default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        allow_mutation=False,
        env='SECRET_KEY',
    )
    algorithm: str = Field(default='HS256', allow_mutation=False, env='ALGORITHM')
    access_token_expire_minutes: int = Field(default=30, allow_mutation=False, env='ACCESS_TOKEN_EXPIRE_MINUTES')

    class Config:
        validate_assignment = True


class AdminCredentials(BaseSettings):
    username: str = Field(default='admin', allow_mutation=False, env='USERNAME_ADMIN')
    first_name: str = Field(default='admin', allow_mutation=False, env='FIRST_NAME_ADMIN')
    second_name: str = Field(default='admin', allow_mutation=False, env='SECOND_NAME_ADMIN')
    email: str = Field(default='admin@example.com', allow_mutation=False, env='EMAIL_ADMIN')
    password: str = Field(default='admin', allow_mutation=False, env='PASSWORD_ADMIN')

    class Config:
        validate_assignment = True


class KafkaConfig(BaseSettings):
    topic: str = Field(default='identity_provider', env='IDENTITY_PROVIDER_TOPIC')


DB_CONFIG: DBConfig = DBConfig()
AUTH_CONFIG: AuthConfig = AuthConfig()
ADMIN_CREDS: AdminCredentials = AdminCredentials()
KAFKA_CONFIG: KafkaConfig = KafkaConfig()
