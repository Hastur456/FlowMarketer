from fastapi_users.authentication import (
    BearerTransport, 
    CookieTransport
)


bearretransport = BearerTransport(
    tokenUrl="auth/jwt/login"
)

cookie_transport = CookieTransport(
    cookie_name="access_token",
    cookie_max_age=3600,
    cookie_secure=True,
    cookie_httponly=True,
    cookie_samesite="lax",
)
