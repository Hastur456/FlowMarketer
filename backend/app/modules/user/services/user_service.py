from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.models import User, UserAddress
from app.modules.user.schemas import UserRead, UserUpdate, AddressCreate
from app.modules.user.adapters.db_adapter.user_repository import UserRepository
from app.core.exceptions import NotFoundException


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_profile(self, session: AsyncSession, user_id: UUID) -> UserRead:
        user = await self.user_repo.find_by_id(session, user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserRead.model_validate(user)

    async def update_profile(self, user_id: UUID, data: UserUpdate) -> UserRead:
        updated_user = await self.user_repo.update(user_id, data.dict(exclude_unset=True))
        return UserRead.model_validate(updated_user)

    async def add_address(self, user_id: UUID, data: AddressCreate):
        addresses = await self.user_repo.get_addresses(user_id)
        is_first = len(addresses) == 0
        
        new_address = UserAddress(**data.dict(), user_id=user_id, is_default=is_first)
        return await self.user_repo.add_address(new_address)
