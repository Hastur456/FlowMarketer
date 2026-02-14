from fastapi import Request
from backend.app.core.logger import get_logger


async def get_es_client(request: Request):
    return request.app.state.es_client

