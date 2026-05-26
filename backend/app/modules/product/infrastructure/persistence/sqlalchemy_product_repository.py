from uuid import UUID

from sqlalchemy import and_, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.logger import logger
from app.infrastructure.db.session import connection
from app.modules.product.domain.entities.product import Product
from app.modules.product.infrastructure.persistence.product_mapper import ProductMapper
from app.modules.product.infrastructure.persistence.product_model import ProductModel


class SqlAlchemyProductRepository:
    model = ProductModel

    @connection(commit=False)
    async def find_by_id(
        self,
        product_id: UUID,
        session: AsyncSession,
    ) -> Product | None:
        try:
            response = await session.execute(
                select(self.model).where(self.model.id == product_id)
            )
            model = response.scalar_one_or_none()
            return ProductMapper.to_domain(model) if model else None
        except SQLAlchemyError as error:
            logger.error("Error finding product by id %s: %s", product_id, error)
            raise

    @connection(commit=False)
    async def find_by_category(
        self,
        category_id: UUID,
        session: AsyncSession,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Product]:
        try:
            query = (
                select(self.model)
                .where(
                    and_(
                        self.model.category_id == category_id,
                        self.model.is_active.is_(True),
                    )
                )
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            return [ProductMapper.to_domain(model) for model in response.scalars().all()]
        except SQLAlchemyError as error:
            logger.error("Error finding products by category %s: %s", category_id, error)
            raise

    @connection(commit=False)
    async def find_active(
        self,
        session: AsyncSession,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Product]:
        try:
            query = (
                select(self.model)
                .where(self.model.is_active.is_(True))
                .order_by(desc(self.model.created_at))
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            return [ProductMapper.to_domain(model) for model in response.scalars().all()]
        except SQLAlchemyError as error:
            logger.error("Error finding active products: %s", error)
            raise

    @connection(commit=False)
    async def find_featured(
        self,
        session: AsyncSession,
        limit: int = 10,
    ) -> list[Product]:
        try:
            query = (
                select(self.model)
                .where(
                    and_(
                        self.model.is_active.is_(True),
                        self.model.is_featured.is_(True),
                    )
                )
                .limit(limit)
            )
            response = await session.execute(query)
            return [ProductMapper.to_domain(model) for model in response.scalars().all()]
        except SQLAlchemyError as error:
            logger.error("Error finding featured products: %s", error)
            raise

    @connection(commit=False)
    async def find_by_price_range(
        self,
        session: AsyncSession,
        min_price: float = 0,
        max_price: float | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Product]:
        try:
            conditions = [
                self.model.is_active.is_(True),
                self.model.price >= min_price,
            ]

            if max_price is not None:
                conditions.append(self.model.price <= max_price)

            query = (
                select(self.model)
                .where(and_(*conditions))
                .limit(limit)
                .offset(offset)
            )
            response = await session.execute(query)
            return [ProductMapper.to_domain(model) for model in response.scalars().all()]
        except SQLAlchemyError as error:
            logger.error("Error finding products by price range: %s", error)
            raise

    @connection(commit=True)
    async def create(
        self,
        product: Product,
        session: AsyncSession,
    ) -> Product:
        try:
            model = ProductMapper.to_model(product)
            session.add(model)
            await session.flush()
            await session.refresh(model)
            return ProductMapper.to_domain(model)
        except SQLAlchemyError as error:
            logger.error("Error creating product: %s", error)
            raise

    @connection(commit=True)
    async def update(
        self,
        product_id: UUID,
        updates: Product | dict,
        session: AsyncSession,
    ) -> Product | None:
        try:
            response = await session.execute(
                select(self.model).where(self.model.id == product_id)
            )
            model = response.scalar_one_or_none()

            if model is None:
                return None

            ProductMapper.update_model(model, updates)
            await session.flush()
            await session.refresh(model)
            return ProductMapper.to_domain(model)
        except SQLAlchemyError as error:
            logger.error("Error updating product %s: %s", product_id, error)
            raise

    @connection(commit=True)
    async def delete(
        self,
        product_id: UUID,
        session: AsyncSession,
    ) -> Product | None:
        try:
            response = await session.execute(
                select(self.model).where(self.model.id == product_id)
            )
            model = response.scalar_one_or_none()

            if model is None:
                return None

            product = ProductMapper.to_domain(model)
            await session.delete(model)
            await session.flush()
            return product
        except SQLAlchemyError as error:
            logger.error("Error deleting product %s: %s", product_id, error)
            raise

    @connection(commit=True)
    async def update_stock(
        self,
        product_id: UUID,
        quantity_change: int,
        session: AsyncSession,
    ) -> Product | None:
        try:
            response = await session.execute(
                select(self.model).where(self.model.id == product_id)
            )
            model = response.scalar_one_or_none()

            if model is None:
                return None

            model.stock_quantity = max(0, model.stock_quantity + quantity_change)
            await session.flush()
            await session.refresh(model)
            return ProductMapper.to_domain(model)
        except SQLAlchemyError as error:
            logger.error("Error updating product stock %s: %s", product_id, error)
            raise
