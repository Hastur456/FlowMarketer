from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from backend.app.infrastructure.db.base_repository import BaseRepository
from backend.app.modules.cart.models import CartItem
from db.session import connection
from backend.app.core.logger import logger


class CartRepository(BaseRepository):
    """
    Репозиторий для работы с корзиной покупок
    
    Методы:
    - find_by_user() - получение товаров в корзине пользователя
    - add_item() - добавление товара в корзину
    - remove_item() - удаление товара из корзины
    - update_quantity() - обновление количества товара в корзине
    - clear_cart() - очистка корзины пользователя
    - get_total() - получение общей стоимости корзины
    """
    
    model = CartItem

    @classmethod
    @connection(commit=False)
    async def find_by_user(cls, session: AsyncSession, user_id: str):
        """Получение товаров в корзине пользователя"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.user_id == user_id)
                .order_by(cls.model.created_at)
            )
            response = await session.execute(query)
            items = response.scalars().all()

            logger.info(f"Найдено {len(items)} товаров в корзине пользователя {user_id}")
            return items
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении корзины пользователя {user_id}: {e}")
            raise

    @classmethod
    @connection(commit=True)
    async def update_quantity(
        cls,
        session: AsyncSession,
        cart_item_id: str,
        new_quantity: int
    ):
        """Обновление количества товара в корзине"""
        try:
            query = select(cls.model).where(cls.model.id == cart_item_id)
            response = await session.execute(query)
            item = response.scalar_one_or_none()

            if not item:
                logger.warning(f"Товар в корзине с ID {cart_item_id} не найден")
                return None

            item.quantity = new_quantity
            item.updated_at = datetime.utcnow()

            await session.flush()
            await session.refresh(item)

            logger.info(f"Количество товара в корзине {cart_item_id} обновлено на {new_quantity}")
            return item

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при обновлении количества товара в корзине {cart_item_id}: {e}")
            raise

    @classmethod
    @connection(commit=True)
    async def clear_cart(cls, session: AsyncSession, user_id: str):
        """Очистка корзины пользователя"""
        try:
            query = select(cls.model).where(cls.model.user_id == user_id)
            response = await session.execute(query)
            items = response.scalars().all()

            for item in items:
                await session.delete(item)

            await session.flush()

            logger.info(f"Корзина пользователя {user_id} очищена")
            return True

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при очистке корзины пользователя {user_id}: {e}")
            raise
