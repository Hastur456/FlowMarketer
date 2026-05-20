from functools import wraps
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import database_url


engine = create_async_engine(url=database_url)
session_maker = async_sessionmaker(engine, expire_on_commit=False)

_test_session_maker: async_sessionmaker | None = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        try:
            yield session

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()


def connection(commit: bool = False):
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            maker = _test_session_maker or session_maker
            
            async with maker() as session:
                try:
                    result = await method(*args, session=session, **kwargs)
                    
                    if commit:
                        await session.commit()
                    
                    return result
                
                except Exception:
                    await session.rollback()
                    raise
                
                finally:
                    await session.close()
        
        return wrapper
    return decorator


def set_test_session_maker(maker: async_sessionmaker | None = None):
    global _test_session_maker
    _test_session_maker = maker
