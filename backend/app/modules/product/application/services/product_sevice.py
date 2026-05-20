from logging import Logger
from typing import List
from uuid import UUID
from elasticsearch import AsyncElasticsearch

from app.core.logger import logger
from app.modules.product.domain.entities.product import Product
from app.modules.product.adapters.es_adapter.product_indexer import ProductIndexer
from app.modules.product.adapters.es_adapter.product_searcher import ProductSearcher
from app.modules.product.adapters.db_adapter.product_repository import ProductRepository


class ProductService:
    def __init__(
        self,
        es: AsyncElasticsearch,
        logger: Logger = logger,
    ):
        self.logger = logger
        self.repository = ProductRepository()
        self.indexer = ProductIndexer(es, logger)
        self.searcher = ProductSearcher(es, logger)

    async def initialize(self):
        await self.indexer.create_index()

    async def search_products(self, **kwargs):
        results = await self.searcher.search_with_filters(**kwargs)
        return [r.model_dump() for r in results]

    async def autocomplete(self, prefix: str):
        return await self.searcher.autocomplete(prefix)

    async def get_product(self, product_id: UUID):
        product = await self.repository.find_by_id(product_id)
        if not product:
            return None
        return product

    async def get_products_by_category(self, category_id: int, limit: int = 50, offset: int = 0):
        return await self.repository.find_by_category(
            category_id=category_id,
            limit=limit,
            offset=offset,
        )

    async def create_product(self, data: Product):
        product = await self.repository.create(**data)
        await self.indexer.index_one(product.model_dump())
        return product

    async def bulk_create_products(self, products: List[Product]):
        created = []
        for data in products:
            product = await self.repository.create(**data)
            created.append(product.model_dump())
        await self.indexer.bulk_index(created)
        return created

    async def update_product(self, product_id: int, updates: dict):
        product = await self.repository.update(product_id, **updates)
        if not product:
            return None
        await self.indexer.update_one(product_id, updates)
        return product

    async def delete_product(self, product_id: int):
        product = await self.repository.delete(product_id)
        if not product:
            return None
        await self.indexer.delete_one(product_id)
        return product

    async def update_stock(self, product_id: int, quantity_change: int):
        product = await self.repository.update_stock(
            product_id=product_id,
            quantity_change=quantity_change,
        )
        if product:
            await self.indexer.update_one(product_id, {"stock": product.stock})
        return product

    async def reindex_product(self, product_id: int):
        product = await self.repository.find_by_id(product_id)
        if not product:
            return None
        await self.indexer.index_one(product.model_dump())
        return product

    async def rebuild_index(self):
        products = await self.repository.find_active(limit=100000, offset=0)
        docs = [p.model_dump() for p in products]
        await self.indexer.bulk_index(docs)
        return len(docs)
