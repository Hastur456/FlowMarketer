from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.repositories.base_repository import BaseRepository
from app.models.review import Review
from database.session import connection
from app.utils.logger import logger


class ReviewRepository(BaseRepository):
    """
    Репозиторий для работы с отзывами о товарах
    
    Методы:
    - find_by_id() - поиск отзыва по ID
    - find_by_product() - получение отзывов о товаре
    - find_by_user() - получение отзывов пользователя
    - find_by_rating() - получение отзывов по рейтингу
    - create() - создание отзыва
    - update() - обновление отзыва
    - delete() - удаление отзыва
    - get_average_rating() - получение средней оценки товара
    """
    
    model = Review

    @classmethod
    @connection(commit=False)
    async def find_by_product(
        cls,
        session: AsyncSession,
        product_id: str,
        limit: int = 20,
        offset: int = 0
    ):
        """Получение отзывов о товаре"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.product_id == product_id)
                .order_by(desc(cls.model.created_at))
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            reviews = response.scalars().all()

            logger.info(f"Найдено {len(reviews)} отзывов о товаре {product_id}")
            return reviews
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении отзывов о товаре {product_id}: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def find_by_user(cls, session: AsyncSession, user_id: str):
        """Получение отзывов пользователя"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.user_id == user_id)
                .order_by(desc(cls.model.created_at))
            )
            response = await session.execute(query)
            reviews = response.scalars().all()

            logger.info(f"Найдено {len(reviews)} отзывов пользователя {user_id}")
            return reviews
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении отзывов пользователя {user_id}: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def find_by_rating(
        cls,
        session: AsyncSession,
        rating: int,
        limit: int = 50,
        offset: int = 0
    ):
        """Получение отзывов по рейтингу"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.rating == rating)
                .order_by(desc(cls.model.created_at))
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            reviews = response.scalars().all()

            logger.info(f"Найдено {len(reviews)} отзывов с рейтингом {rating}")
            return reviews
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении отзывов с рейтингом {rating}: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def get_average_rating(cls, session: AsyncSession, product_id: str):
        """Получение средней оценки товара"""
        try:
            query = (
                select(func.avg(cls.model.rating))
                .where(cls.model.product_id == product_id)
            )
            response = await session.execute(query)
            average = response.scalar_one_or_none()

            logger.info(f"Средняя оценка товара {product_id}: {average}")
            return round(average, 2) if average else 0
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении средней оценки товара {product_id}: {e}")
            raise
