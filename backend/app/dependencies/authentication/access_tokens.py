from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.access_token import AccessToken
from app.database.session import get_session


async def get_access_tokens_db(
    session: AsyncSession = Depends(get_session)
):
    yield AccessToken.get_db(session=session)
