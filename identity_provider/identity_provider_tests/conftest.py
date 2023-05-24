import pytest


@pytest.fixture
def identity_provider_api() -> str:
    return 'identity_provider'


@pytest.fixture
def identity_provider_port() -> int:
    return 8030


@pytest.fixture
def base_url(identity_provider_api: str, identity_provider_port: int) -> str:
    return f'http://{identity_provider_api}:{identity_provider_port}'
