from typing import Dict


class ValidationError(Exception):
    pass


class ServiceNotAvailableError(Exception):
    pass


class AccessDenied(Exception):
    pass


class NotFoundError(Exception):
    def __init__(self, content: Dict):
        super().__init__()
        self.content: Dict = content


class UnauthorizedError(Exception):
    def __init__(self, details: str):
        super().__init__()
        self.details: str = details
