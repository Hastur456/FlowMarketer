from logging import Logger
from typing import Any, Dict, AsyncIterable, Mapping, Tuple, Union

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_streaming_bulk
from elasticsearch.exceptions import ApiError

from app.modules.product.infrastructure.search.product_index import ProductIndexConfig
from app.modules.product.infrastructure.search.product_mapper import ProductMapper, ProductSource


ProductInput = Union[ProductSource, Mapping[str, Any]]


class ProductIndexer:
    """Асинхронное управление индексом products."""
    
    def __init__(self, es_client: AsyncElasticsearch, logger: Logger):
        self.es = es_client
        self.logger = logger
        self.index_name = ProductIndexConfig.INDEX_NAME
    
    async def create_index(self) -> bool:
        """Создать индекс (асинхронно)."""
        try:
            exists = await self.es.indices.exists(index=self.index_name)
            if exists:
                self.logger.info("Index '%s' already exists", self.index_name)
                return True
            
            await self.es.indices.create(
                index=self.index_name,
                body=ProductIndexConfig.get_mapping()
            )
            self.logger.info("✓ Index '%s' created", self.index_name)
            return True
        
        except ApiError as e:
            self.logger.error("Error creating index: %s", e)
            raise
    
    async def index_one(self, product: ProductInput) -> bool:
        """Индексировать один товар (асинхронно)."""
        doc = ProductMapper.to_es_document(product)
        product_id = int(doc["id"])
        
        try:
            await self.es.index(
                index=self.index_name,
                id=product_id,
                document=doc,
                refresh=False
            )
            self.logger.debug("Product %s indexed", product_id)
            return True
        
        except ApiError as e:
            self.logger.error("Error indexing product %s: %s", product_id, e)
            raise
    
    async def bulk_index(
        self, 
        products: AsyncIterable[ProductInput] | list[ProductInput]
    ) -> Tuple[int, int]:
        """Массовое индексирование (асинхронно)."""
        
        async def _actions():
            """Генератор действий для bulk."""
            # Если list → преобразуем в async iterator
            items = products if hasattr(products, '__aiter__') else products
            
            async for item in items if hasattr(products, '__aiter__') else (
                (x for x in products)
            ):
                doc = ProductMapper.to_es_document(item)
                yield {
                    "_op_type": "index",
                    "_index": self.index_name,
                    "_id": int(doc["id"]),
                    "_source": doc,
                }
        
        success_count = 0
        error_count = 0
        
        try:
            async for ok, result in async_streaming_bulk(
                client=self.es,
                actions=_actions(),
                raise_on_error=False,
                raise_on_exception=False,
                chunk_size=500,
            ):
                if ok:
                    success_count += 1
                else:
                    error_count += 1
                    if error_count <= 5:
                        self.logger.warning("Bulk error: %s", result)
            
            self.logger.info("✓ Bulk indexed %s (%s errors)", success_count, error_count)
            return success_count, error_count
        
        except ApiError as e:
            self.logger.error("Bulk indexing failed: %s", e)
            raise
    
    async def update_one(self, product_id: int, partial: Dict[str, Any]) -> bool:
        """Partial update товара (асинхронно)."""
        try:
            await self.es.update(
                index=self.index_name,
                id=product_id,
                doc=partial,
                refresh=False
            )
            self.logger.debug("Product %s updated", product_id)
            return True
        
        except ApiError as e:
            self.logger.error("Error updating product %s: %s", product_id, e)
            raise
    
    async def delete_one(self, product_id: int) -> bool:
        """Удалить товар (асинхронно)."""
        try:
            await self.es.delete(
                index=self.index_name,
                id=product_id,
                refresh=False
            )
            self.logger.debug("Product %s deleted", product_id)
            return True
        
        except ApiError as e:
            self.logger.error("Error deleting product %s: %s", product_id, e)
            raise
    
    async def refresh(self) -> bool:
        """Обновить индекс (асинхронно)."""
        try:
            await self.es.indices.refresh(index=self.index_name)
            return True
        except ApiError as e:
            self.logger.error("Error refreshing index: %s", e)
            raise
