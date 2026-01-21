from fastapi_users.authentication import AuthenticationBackend
from app.core.authentication.transport import (
    bearretransport,
    cookie_transport
)

from .strategy import get_database_strategy


authentication_backend = AuthenticationBackend(
    name="accesstokens",
    transport=cookie_transport,
    get_strategy=get_database_strategy
)
