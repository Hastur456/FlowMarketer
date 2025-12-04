from sqlalchemy.ext.asyncio import create_async_engine

from database.base import Base
from config import database_url


engine = create_async_engine(url=database_url)
