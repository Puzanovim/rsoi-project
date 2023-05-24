from pydantic import BaseSettings, Field


class NotesConfig(BaseSettings):
    host: str = Field(env='NOTES_SERVICE_HOST', default='notes_service')
    port: int = Field(env='NOTES_SERVICE_PORT', default=8070)

    class Config:
        validate_assignment = True


class CategoryConfig(BaseSettings):
    host: str = Field(env='CATEGORY_SERVICE_HOST', default='category_service')
    port: int = Field(env='CATEGORY_SERVICE_PORT', default=8060)

    class Config:
        validate_assignment = True


class NamespaceConfig(BaseSettings):
    host: str = Field(env='NAMESPACE_SERVICE_HOST', default='namespace_service')
    port: int = Field(env='NAMESPACE_SERVICE_PORT', default=8050)

    class Config:
        validate_assignment = True


class StatisticConfig(BaseSettings):
    host: str = Field(env='STATISTIC_SERVICE_HOST', default='statistic_service')
    port: int = Field(env='STATISTIC_SERVICE_PORT', default=8040)

    class Config:
        validate_assignment = True


class IdentityProviderConfig(BaseSettings):
    host: str = Field(env='IDENTITY_PROVIDER_HOST', default='identity_provider')
    port: int = Field(env='IDENTITY_PROVIDER_PORT', default=8030)

    class Config:
        validate_assignment = True


class CircuitBreakerConfig(BaseSettings):
    failure_threshold: int = Field(env='CIRCUIT_BREAKER_FAILURE_THRESHOLD', default=2)
    success_threshold: int = Field(env='CIRCUIT_BREAKER_SUCCESS_THRESHOLD', default=1)
    timeout: int = Field(env='CIRCUIT_BREAKER_TIMEOUT', default=15)

    class Config:
        validate_assignment = True


NOTES_SERVICE_CONFIG: NotesConfig = NotesConfig()
CATEGORY_SERVICE_CONFIG: CategoryConfig = CategoryConfig()
NAMESPACE_SERVICE_CONFIG: NamespaceConfig = NamespaceConfig()
STATISTIC_SERVICE_CONFIG: StatisticConfig = StatisticConfig()
IDENTITY_PROVIDER_CONFIG: IdentityProviderConfig = IdentityProviderConfig()
CIRCUIT_BREAKER_CONFIG: CircuitBreakerConfig = CircuitBreakerConfig()
