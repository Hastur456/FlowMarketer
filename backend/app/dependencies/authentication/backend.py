from fastapi_users.authentication import AuthenticationBackend
from app.core.authentication.transport import (
    bearretransport,
    cookietransport
)

from .strategy import get_database_strategy


authentication_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=cookietransport,
    get_strategy=get_database_strategy
)
