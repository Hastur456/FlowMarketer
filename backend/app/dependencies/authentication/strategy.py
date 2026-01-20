from fastapi import Depends
from fastapi_users.authentication.strategy.db import (
    DatabaseStrategy,
    AccessTokenDatabase
)

from .access_tokens import get_access_tokens_db
from app.database.models.access_token import AccessToken


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_tokens_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db, # Передаем полученную через Depends базу
        lifetime_seconds=3600 # Увеличьте, 360 сек — это очень мало (6 мин)
    )