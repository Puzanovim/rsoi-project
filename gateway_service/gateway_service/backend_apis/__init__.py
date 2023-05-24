from gateway_service.backend_apis.category_service_api.category_service_api import CategoryServiceAPI
from gateway_service.backend_apis.identity_provider_api.identity_provider_api import IdentityProviderAPI
from gateway_service.backend_apis.namespace_service_api.namespace_service_api import NamespaceServiceAPI
from gateway_service.backend_apis.notes_service_api.notes_service_api import NotesServiceAPI
from gateway_service.backend_apis.statistics_service_api.statistics_service_api import StatisticsServiceAPI

notes_service_api: NotesServiceAPI = NotesServiceAPI()
category_service_api: CategoryServiceAPI = CategoryServiceAPI()
namespace_service_api: NamespaceServiceAPI = NamespaceServiceAPI()
identity_provider_api: IdentityProviderAPI = IdentityProviderAPI()
statistics_service_api: StatisticsServiceAPI = StatisticsServiceAPI()


async def get_notes_service_api() -> NotesServiceAPI:
    return notes_service_api


async def get_category_service_api() -> CategoryServiceAPI:
    return category_service_api


async def get_namespace_service_api() -> NamespaceServiceAPI:
    return namespace_service_api


async def get_identity_provider_api() -> IdentityProviderAPI:
    return identity_provider_api


async def get_statistics_service_api() -> StatisticsServiceAPI:
    return statistics_service_api
