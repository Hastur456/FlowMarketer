from fastapi_users.authentication import BearerTransport


bearretransport = BearerTransport(
    tokenUrl="auth/jwt/login"
)
