from pydantic import BaseSettings, Field


class DBConfig(BaseSettings):
    db_user: str = Field(default='program', allow_mutation=False, env='DB_USER')
    db_password: str = Field(default='test', allow_mutation=False, env='DB_PASS')
    db_host: str = Field(default='postgres', allow_mutation=False, env='DB_HOST')
    db_port: int = Field(default=5432, allow_mutation=False, env='DB_PORT')
    db_name: str = Field(default='statistics', allow_mutation=False, env='DB_NAME')

    class Config:
        validate_assignment = True


class AuthConfig(BaseSettings):
    jwt_key: str = Field(
        default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        allow_mutation=False,
        env='SECRET_KEY',
    )
    algorithm: str = Field(default='HS256', allow_mutation=False, env='ALGORITHM')

    class Config:
        validate_assignment = True


DB_CONFIG: DBConfig = DBConfig()
AUTH_CONFIG: AuthConfig = AuthConfig()
