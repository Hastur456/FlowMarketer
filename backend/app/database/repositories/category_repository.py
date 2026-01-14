from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from backend.app.database.repositories.base_repository import BaseRepository
from app.models.category import Category
from database.session import connection
from app.utils.logger import logger


class CategoryRepository(BaseRepository):
    """
    Репозиторий для работы с категориями товаров
    
    Методы:
    - find_by_id() - поиск категории по ID
    - find_by_slug() - поиск категории по slug
    - find_all() - получение всех категорий
    - create() - создание категории
    - update() - обновление категории
    - delete() - удаление категории
    """
    
    model = Category

    @classmethod
    @connection(commit=False)
    async def find_by_slug(cls, session: AsyncSession, slug: str):
        """Поиск категории по slug"""
        try:
            query = select(cls.model).where(cls.model.slug == slug)
            response = await session.execute(query)
            category = response.scalar_one_or_none()

            if category:
                logger.info(f"Найдена категория с slug {slug}")
            else:
                logger.info(f"Категория с slug {slug} не найдена")

            return category
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске категории по slug {slug}: {e}")
            raise
