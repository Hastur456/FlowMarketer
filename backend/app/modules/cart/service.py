from logging import Logger
from uuid import UUID

from elasticsearch import AsyncElasticsearch

from app.modules.product.infrastructure.search.product_indexer import ProductIndexer
from app.modules.product.infrastructure.search.product_searcher import ProductSearcher


class ProductService:
    def __init__(
        self,
        es: AsyncElasticsearch,
        logger: Logger,
    ):
        self.logger = logger
        self.indexer = ProductIndexer(es, logger)
        self.searcher = ProductSearcher(es, logger)

    async def initialize(self) -> None:
        await self.indexer.create_index()

    async def search_products(self, **kwargs):
        results = await self.searcher.search_with_filters(**kwargs)
        return [r.model_dump() for r in results]

    async def autocomplete(self, prefix: str):
        return await self.searcher.autocomplete(prefix)

    async def index_product(self, product: dict):
        return await self.indexer.index_one(product)

    async def bulk_index_products(self, products: list[dict]):
        return await self.indexer.bulk_index(products)

    async def update_product(self, product_id: UUID, updates: dict):
        return await self.indexer.update_one(product_id, updates)

    async def delete_product(self, product_id: UUID):
        return await self.indexer.delete_one(product_id)

