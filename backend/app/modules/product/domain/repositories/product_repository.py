from typing import Protocol, runtime_checkable
from uuid import UUID

from app.modules.product.domain.entities.product import Product


@runtime_checkable
class ProductRepository(Protocol):
    async def find_by_category(
        self,
        category_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Product]:
        ...

    async def find_active(self, limit: int = 50, offset: int = 0) -> list[Product]:
        ...

    async def find_featured(self, limit: int = 10) -> list[Product]:
        ...

    async def find_by_price_range(
        self,
        min_price: float = 0,
        max_price: float | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Product]:
        ...

    async def update_stock(self, product_id: UUID, quantity_change: int) -> Product | None:
        ...
