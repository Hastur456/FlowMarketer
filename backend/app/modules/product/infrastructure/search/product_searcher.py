"""Асинхронный поисковик товаров."""

from __future__ import annotations

from logging import Logger
from typing import Any, Dict, List
from fastapi import Depends
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ApiError

from app.modules.product.infrastructure.search.product_index import ProductIndexConfig
from app.modules.product.infrastructure.search.product_mapper import ProductMapper, ProductESDocument
from app.infrastructure.elasticsearch.es_depends import get_es_client


class ProductSearcher:
    """Асинхронный поиск товаров."""
    
    def __init__(
        self,
        logger: Logger,
        es_client: AsyncElasticsearch = Depends(get_es_client)
    ):
        self.es = es_client
        self.logger = logger
        self.index_name = ProductIndexConfig.INDEX_NAME
    
    async def search_by_text(
        self,
        query: str,
        size: int = 10,
        from_: int = 0,
    ) -> List[ProductESDocument]:
        """Полнотекстовый поиск (асинхронно)."""
        try:
            body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name^3", "search_text", "description"],
                    }
                },
                "from": from_,
                "size": size,
            }
            
            response = await self.es.search(index=self.index_name, body=body)
            
            hits = response.get("hits", {}).get("hits", [])
            return [ProductMapper.from_es_hit(hit) for hit in hits]
        
        except ApiError as e:
            self.logger.error("Search error: %s", e)
            raise
    
    async def filter_by_category(
        self,
        category_id: int,
        size: int = 20,
    ) -> List[ProductESDocument]:
        """Фильтр по категории (асинхронно)."""
        try:
            body = {
                "query": {
                    "term": {"category_id": category_id}
                },
                "size": size,
            }
            
            response = await self.es.search(index=self.index_name, body=body)
            hits = response.get("hits", {}).get("hits", [])
            return [ProductMapper.from_es_hit(hit) for hit in hits]
        
        except ApiError as e:
            self.logger.error("Filter error: %s", e)
            raise
    
    async def search_with_filters(
        self,
        query: str,
        min_price: float = None,
        max_price: float = None,
        in_stock: bool = True,
        size: int = 10,
    ) -> List[ProductESDocument]:
        """Поиск с фильтрами (асинхронно)."""
        filters = []
        
        if in_stock:
            filters.append({"term": {"is_available": True}})
        
        if min_price is not None:
            filters.append({"range": {"price": {"gte": min_price}}})
        
        if max_price is not None:
            filters.append({"range": {"price": {"lte": max_price}}})
        
        try:
            body: Dict[str, Any] = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["name^3", "search_text"],
                                }
                            }
                        ],
                        "filter": filters,
                    }
                },
                "size": size,
            }
            
            response = await self.es.search(index=self.index_name, body=body)
            hits = response.get("hits", {}).get("hits", [])
            return [ProductMapper.from_es_hit(hit) for hit in hits]
        
        except ApiError as e:
            self.logger.error("Filtered search error: %s", e)
            raise
    
    async def autocomplete(self, prefix: str, size: int = 5) -> List[str]:
        """Автодополнение (асинхронно)."""
        try:
            body = {
                "query": {
                    "match_phrase_prefix": {
                        "name": {"query": prefix}
                    }
                },
                "_source": ["name"],
                "size": size,
            }
            
            response = await self.es.search(index=self.index_name, body=body)
            hits = response.get("hits", {}).get("hits", [])
            return [hit["_source"]["name"] for hit in hits]
        
        except ApiError as e:
            self.logger.error("Autocomplete error: %s", e)
            raise
