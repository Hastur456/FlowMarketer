from logging import Logger
from typing import Any, Dict, List

from app.elasticsearch.client import ElasticsearchClient
from app.elasticsearch.indexers.product_indexer import ProductIndexer
from app.elasticsearch.searchers.product_searcher import ProductSearcher
from app.elasticsearch.mappers.product_mapper import ProductMapper, ProductSource


class ProductService:
    """
    Асинхронный сервис товаров.
    Координирует: поиск, индексирование, маппинг.
    """
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self._es_client = None
        self._indexer = None
        self._searcher = None
    
    async def _ensure_initialized(self) -> None:
        """Инициализировать компоненты (если ещё не инициализированы)."""
        if self._es_client is None:
            self._es_client = await ElasticsearchClient.connect()
            self._indexer = ProductIndexer(self._es_client, self.logger)
            self._searcher = ProductSearcher(self._es_client, self.logger)
    
    @property
    async def indexer(self) -> ProductIndexer:
        """Получить indexer."""
        await self._ensure_initialized()
        return self._indexer
    
    @property
    async def searcher(self) -> ProductSearcher:
        """Получить searcher."""
        await self._ensure_initialized()
        return self._searcher
    
    async def initialize(self) -> None:
        """Инициализировать ES (создать индексы)."""
        indexer = await self.indexer
        await indexer.create_index()
    
    async def search_products(
        self,
        query: str,
        min_price: float = None,
        max_price: float = None,
        in_stock: bool = True,
        size: int = 10,
    ) -> List[Dict[str, Any]]:
        """Поиск товаров (асинхронно)."""
        searcher = await self.searcher
        results = await searcher.search_with_filters(
            query=query,
            min_price=min_price,
            max_price=max_price,
            in_stock=in_stock,
            size=size,
        )
        return [result.model_dump() for result in results]
    
    async def autocomplete(self, prefix: str) -> List[str]:
        """Автодополнение (асинхронно)."""
        searcher = await self.searcher
        return await searcher.autocomplete(prefix)
    
    async def index_product(self, product_dict: Dict[str, Any]) -> bool:
        """Индексировать товар (асинхронно)."""
        product = ProductSource.model_validate(product_dict)
        indexer = await self.indexer
        return await indexer.index_one(product)
    
    async def bulk_index_products(
        self, 
        products: List[Dict[str, Any]]
    ) -> tuple:
        """Массовое индексирование (асинхронно)."""
        product_sources = [
            ProductSource.model_validate(p) for p in products
        ]
        indexer = await self.indexer
        return await indexer.bulk_index(product_sources)
    
    async def update_product(
        self, 
        product_id: int, 
        updates: Dict[str, Any]
    ) -> bool:
        """Обновить товар (асинхронно)."""
        indexer = await self.indexer
        return await indexer.update_one(product_id, updates)
    
    async def delete_product(self, product_id: int) -> bool:
        """Удалить товар (асинхронно)."""
        indexer = await self.indexer
        return await indexer.delete_one(product_id)
    
    async def close(self) -> None:
        """Закрыть соединение с ES."""
        await ElasticsearchClient.close()
