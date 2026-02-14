from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from backend.app.infrastructure.db.base_repository import BaseRepository
from app.infrastructure.db.models.payment import Payment
from db.session import connection
from backend.app.core.logger import logger


class PaymentRepository(BaseRepository):
    """
    Репозиторий для работы с платежами
    
    Методы:
    - find_by_id() - поиск платежа по ID
    - find_by_order() - получение платежа по заказу
    - find_by_status() - получение платежей по статусу
    - find_by_method() - получение платежей по методу
    - find_pending() - получение неокончательных платежей
    - create() - создание платежа
    - update() - обновление платежа
    - update_status() - обновление статуса платежа
    - delete() - удаление платежа
    """
    
    model = Payment

    @classmethod
    @connection(commit=False)
    async def find_by_order(cls, session: AsyncSession, order_id: str):
        """Получение платежа по заказу"""
        try:
            query = select(cls.model).where(cls.model.order_id == order_id)
            response = await session.execute(query)
            payment = response.scalar_one_or_none()

            if payment:
                logger.info(f"Найден платеж для заказа {order_id}")
            else:
                logger.info(f"Платеж для заказа {order_id} не найден")

            return payment
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении платежа для заказа {order_id}: {e}")
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
        """Получение платежей по статусу"""
        try:
            query = (
                select(cls.model)
                .where(cls.model.status == status)
                .order_by(desc(cls.model.created_at))
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            payments = response.scalars().all()

            logger.info(f"Найдено {len(payments)} платежей со статусом {status}")
            return payments
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении платежей со статусом {status}: {e}")
            raise

    @classmethod
    @connection(commit=True)
    async def update_status(
        cls,
        session: AsyncSession,
        payment_id: str,
        new_status: str
    ):
        """Обновление статуса платежа"""
        try:
            query = select(cls.model).where(cls.model.id == payment_id)
            response = await session.execute(query)
            payment = response.scalar_one_or_none()

            if not payment:
                logger.warning(f"Платеж с ID {payment_id} не найден")
                return None

            old_status = payment.status
            payment.status = new_status
            payment.updated_at = datetime.utcnow()

            await session.flush()
            await session.refresh(payment)

            logger.info(f"Статус платежа {payment_id} изменен с {old_status} на {new_status}")
            return payment

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при обновлении статуса платежа {payment_id}: {e}")
            raise
