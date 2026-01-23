from contextlib import asynccontextmanager, AsyncExitStack
from fastapi import FastAPI

from app.core.elasticsearch.lifespan import es_lifespan
from app.database.lifespan import db_lifespan


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncExitStack() as stack:
        await stack.enter_async_context(db_lifespan(app))
        # await stack.enter_async_context(es_lifespan(app))
        yield
