from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.base_repository import BaseRepository
from app.models.product import Product
from database.session import connection
from app.utils.logger import logger


class ProductRepository(BaseRepository):
    """
    Репозиторий для работы с товарами
    
    Методы:
    - find_by_id() - поиск товара по ID
    - find_all() - получение всех товаров с фильтрацией
    - find_by_category() - получение товаров по категории
    - find_active() - получение активных товаров
    - find_featured() - получение рекомендуемых товаров
    - find_by_price_range() - поиск по диапазону цен
    - search() - полнотекстовый поиск
    - get_with_reviews() - получение товара с отзывами
    - update_stock() - обновление количества товара
    - create() - создание товара
    - update() - обновление товара
    - delete() - удаление товара
    """
    
    model = Product

    @classmethod
    @connection(commit=False)
    async def find_by_category(
        cls, 
        session: AsyncSession, 
        category_id: str,
        limit: int = 50,
        offset: int = 0
    ):
        """Получение товаров по категории с пагинацией"""
        try:
            query = (
                select(cls.model)
                .where(
                    and_(
                        cls.model.category_id == category_id,
                        cls.model.is_active == True
                    )
                )
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            products = response.scalars().all()

            logger.info(f"Найдено {len(products)} товаров в категории {category_id}")
            return products
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске товаров по категории {category_id}: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def find_active(cls, session: AsyncSession, limit: int = 50, offset: int = 0):
        """Получение активных товаров"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.is_active == True)
                .order_by(desc(cls.model.created_at))
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            products = response.scalars().all()

            logger.info(f"Найдено {len(products)} активных товаров")
            return products
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении активных товаров: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def find_featured(cls, session: AsyncSession, limit: int = 10):
        """Получение рекомендуемых товаров"""
        try:
            query = (
                select(cls.model)
                .where(
                    and_(
                        cls.model.is_active == True,
                        cls.model.is_featured == True
                    )
                )
                .limit(limit)
            )
            response = await session.execute(query)
            products = response.scalars().all()

            logger.info(f"Найдено {len(products)} рекомендуемых товаров")
            return products
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении рекомендуемых товаров: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def find_by_price_range(
        cls,
        session: AsyncSession,
        min_price: float = 0,
        max_price: float = float('inf'),
        limit: int = 50,
        offset: int = 0
    ):
        """Поиск товаров по диапазону цен"""
        try:
            query = (
                select(cls.model)
                .where(
                    and_(
                        cls.model.is_active == True,
                        cls.model.price >= min_price,
                        cls.model.price <= max_price
                    )
                )
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            products = response.scalars().all()

            logger.info(f"Найдено {len(products)} товаров в диапазоне цен {min_price}-{max_price}")
            return products
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске товаров по цене: {e}")
            raise

    @classmethod
    @connection(commit=True)
    async def update_stock(
        cls,
        session: AsyncSession,
        product_id: str,
        quantity_change: int
    ):
        """Обновление количества товара на складе"""
        try:
            query = select(cls.model).where(cls.model.id == product_id)
            response = await session.execute(query)
            product = response.scalar_one_or_none()

            if not product:
                logger.warning(f"Товар с ID {product_id} не найден")
                return None

            product.stock += quantity_change
            
            if product.stock < 0:
                logger.warning(f"Недостаточно товара {product_id} на складе")
                product.stock = 0

            await session.flush()
            await session.refresh(product)

            logger.info(f"Обновлено количество товара {product_id}. Новое количество: {product.stock}")
            return product

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при обновлении количества товара {product_id}: {e}")
            raise
