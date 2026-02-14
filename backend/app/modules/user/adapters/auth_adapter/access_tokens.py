from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.models.access_token import AccessToken
from app.infrastructure.db.session import get_session


async def get_access_tokens_db(
    session: AsyncSession = Depends(get_session)
):
    yield AccessToken.get_db(session=session)
