from fastapi import Request


async def get_es_client(request: Request):
    return request.app.state.es_client

