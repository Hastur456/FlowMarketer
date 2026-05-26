from typing import Protocol
from uuid import UUID

from app.modules.product.domain.entities.product import Product


class ProductRepository(Protocol):
    async def find_by_id(self, product_id: UUID) -> Product | None:
        ...

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

    async def create(self, product: Product) -> Product:
        ...

    async def update(self, product_id: UUID, updates: dict) -> Product | None:
        ...

    async def delete(self, product_id: UUID) -> Product | None:
        ...

    async def update_stock(self, product_id: UUID, quantity_change: int) -> Product | None:
        ...
