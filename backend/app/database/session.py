# app/database/session.py
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.database.engine import engine
from functools import wraps
from typing import Optional


session_maker = async_sessionmaker(engine, expire_on_commit=False)

_test_session_maker: async_sessionmaker | None = None


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
                
                except Exception as e:
                    await session.rollback()
                    raise
                
                finally:
                    await session.close()
        
        return wrapper
    return decorator


def set_test_session_maker(maker: async_sessionmaker | None = None):
    global _test_session_maker
    _test_session_maker = maker
