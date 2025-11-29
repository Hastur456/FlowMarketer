from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["health"]
)


@router.get("/")
async def ping():
    return {
        "message": "pong",
        "status": "success"
    }
