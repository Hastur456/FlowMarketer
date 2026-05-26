from typing import Any, Protocol
from uuid import UUID

from app.modules.product.domain.entities.product import Product


class ProductSearchIndex(Protocol):
    async def create_index(self) -> bool:
        ...

    async def index_one(self, product: Product | dict[str, Any]) -> bool:
        ...

    async def bulk_index(self, products: list[Product | dict[str, Any]]) -> tuple[int, int]:
        ...

    async def update_one(self, product_id: UUID, partial: dict[str, Any]) -> bool:
        ...

    async def delete_one(self, product_id: UUID) -> bool:
        ...
