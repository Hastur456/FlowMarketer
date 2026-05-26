from typing import Protocol
from uuid import UUID


class ProductSearchReader(Protocol):
    async def search_with_filters(
        self,
        query: str,
        min_price: float | None = None,
        max_price: float | None = None,
        in_stock: bool = True,
        size: int = 10,
    ) -> list:
        ...

    async def search_by_text(
        self,
        query: str,
        size: int = 10,
        from_: int = 0,
    ) -> list:
        ...

    async def filter_by_category(self, category_id: UUID, size: int = 20) -> list:
        ...

    async def autocomplete(self, prefix: str, size: int = 5) -> list[str]:
        ...
