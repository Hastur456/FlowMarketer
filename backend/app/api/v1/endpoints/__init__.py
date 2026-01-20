from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from .auth import router as auth_router
from .health import router as health_router


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/v1",
    dependencies=[Depends(http_bearer)]
)

router.include_router(auth_router)
router.include_router(health_router)