from .session import engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def db_lifespan(app):
    yield
    await engine.dispose()