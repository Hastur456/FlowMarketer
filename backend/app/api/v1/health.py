from fastapi import FastAPI, APIRouter


router = APIRouter(prefix="/health")

@router.get("/ping")
def health():
    return {
        "success": "OK",
        "response": "pong"
    }
