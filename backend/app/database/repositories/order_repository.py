from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from backend.app.database.repositories.base_repository import BaseRepository
from app.models.order import Order
from database.session import connection
from app.utils.logger import logger


class OrderRepository(BaseRepository):
    """
    Репозиторий для работы с заказами
    
    Методы:
    - find_by_id() - поиск заказа по ID
    - find_by_user() - получение заказов пользователя
    - find_by_status() - получение заказов по статусу
    - find_pending() - получение неоплаченных заказов
    - get_with_items() - получение заказа с товарами
    - create() - создание заказа
    - update() - обновление заказа
    - update_status() - обновление статуса заказа
    - delete() - удаление заказа
    - count_by_user() - количество заказов пользователя
    """
    
    model = Order

    @classmethod
    @connection(commit=False)
    async def find_by_user(
        cls,
        session: AsyncSession,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ):
        """Получение заказов пользователя"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.user_id == user_id)
                .order_by(desc(cls.model.created_at))
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            orders = response.scalars().all()

            logger.info(f"Найдено {len(orders)} заказов пользователя {user_id}")
            return orders
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении заказов пользователя {user_id}: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def find_by_status(
        cls,
        session: AsyncSession,
        status: str,
        limit: int = 50,
        offset: int = 0
    ):
        """Получение заказов по статусу"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.status == status)
                .order_by(desc(cls.model.created_at))
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            orders = response.scalars().all()

            logger.info(f"Найдено {len(orders)} заказов со статусом {status}")
            return orders
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении заказов со статусом {status}: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def find_pending(cls, session: AsyncSession, limit: int = 50, offset: int = 0):
        """Получение неоплаченных заказов"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.status == "pending")
                .order_by(cls.model.created_at)
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            orders = response.scalars().all()

            logger.info(f"Найдено {len(orders)} неоплаченных заказов")
            return orders
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении неоплаченных заказов: {e}")
            raise

    @classmethod
    @connection(commit=True)
    async def update_status(
        cls,
        session: AsyncSession,
        order_id: str,
        new_status: str
    ):
        """Обновление статуса заказа"""
        try:
            query = select(cls.model).where(cls.model.id == order_id)
            response = await session.execute(query)
            order = response.scalar_one_or_none()

            if not order:
                logger.warning(f"Заказ с ID {order_id} не найден")
                return None

            old_status = order.status
            order.status = new_status
            order.updated_at = datetime.utcnow()

            await session.flush()
            await session.refresh(order)

            logger.info(f"Статус заказа {order_id} изменен с {old_status} на {new_status}")
            return order

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при обновлении статуса заказа {order_id}: {e}")
            raise

    @classmethod
    @connection(commit=False)
    async def count_by_user(cls, session: AsyncSession, user_id: str):
        """Количество заказов пользователя"""
        try:
            query = (
                select(func.count())
                .select_from(cls.model)
                .where(cls.model.user_id == user_id)
            )
            response = await session.execute(query)
            count = response.scalar_one_or_none()

            return count or 0

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при подсчете заказов пользователя {user_id}: {e}")
            raise
