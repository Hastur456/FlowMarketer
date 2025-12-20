from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from backend.app.repositories.base_repository import BaseRepository
from app.models.user import User
from database.session import connection
from app.utils.logger import logger



class UserRepository(BaseRepository):
    """
    Репозиторий для работы с пользователями
    
    Методы:
    - find_by_id() - поиск пользователя по ID
    - find_by_email() - поиск пользователя по email
    - find_all() - получение всех пользователей
    - find_active() - получение активных пользователей
    - find_admins() - получение администраторов
    - create() - создание пользователя
    - update() - обновление данных пользователя
    - delete() - удаление пользователя
    - change_password() - изменение пароля
    - set_admin_status() - установка статуса администратора
    """
    
    model = User

    @classmethod
    @connection(commit=False)
    async def find_by_email(cls, session: AsyncSession, email: str):
        """Поиск пользователя по email"""
        try:
            query = select(cls.model).where(cls.model.email == email)
            response = await session.execute(query)
            user = response.scalar_one_or_none()

            if user:
                logger.info(f"Найден пользователь с email {email}")
            else:
                logger.info(f"Пользователь с email {email} не найден")
            
            return user
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске пользователя по email {email}: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def find_active(cls, session: AsyncSession, limit: int = 50, offset: int = 0):
        """Получение активных пользователей"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.is_active == True)
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            users = response.scalars().all()

            logger.info(f"Найдено {len(users)} активных пользователей")
            return users
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении активных пользователей: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def find_admins(cls, session: AsyncSession):
        """Получение всех администраторов"""
        try:
            query = select(cls.model).where(cls.model.is_admin == True)
            response = await session.execute(query)
            admins = response.scalars().all()

            logger.info(f"Найдено {len(admins)} администраторов")
            return admins
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении администраторов: {e}")
            raise

    @classmethod
    @connection(commit=True)
    async def change_password(
        cls,
        session: AsyncSession,
        user_id: str,
        new_password_hash: str
    ):
        """Изменение пароля пользователя"""
        try:
            query = select(cls.model).where(cls.model.id == user_id)
            response = await session.execute(query)
            user = response.scalar_one_or_none()

            if not user:
                logger.warning(f"Пользователь с ID {user_id} не найден")
                return None

            user.password_hash = new_password_hash
            user.updated_at = datetime.utcnow()

            await session.flush()
            await session.refresh(user)

            logger.info(f"Пароль пользователя {user_id} изменен")
            return user

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при изменении пароля пользователя {user_id}: {e}")
            raise

    @classmethod
    @connection(commit=True)
    async def set_admin_status(
        cls,
        session: AsyncSession,
        user_id: str,
        is_admin: bool
    ):
        """Установка статуса администратора"""
        try:
            query = select(cls.model).where(cls.model.id == user_id)
            response = await session.execute(query)
            user = response.scalar_one_or_none()

            if not user:
                logger.warning(f"Пользователь с ID {user_id} не найден")
                return None

            user.is_admin = is_admin
            user.updated_at = datetime.utcnow()

            await session.flush()
            await session.refresh(user)

            status = "назначен администратором" if is_admin else "лишен прав администратора"
            logger.info(f"Пользователь {user_id} {status}")
            return user

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при установке статуса администратора для {user_id}: {e}")
            raise
