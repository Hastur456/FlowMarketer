from elasticsearch import Elasticsearch
from app.schemas.search import SearchQuery, SearchResult
from typing import Dict, Any, List, Optional
from utils.logger import logger
import time


class ElasticsearchSearcher:
    """Поиск в Elasticsearch"""
    
    def __init__(self, es_client: Elasticsearch):
        self.es = es_client
        self.products_index = "products"
    
    def search_products(self, search_query: SearchQuery) -> SearchResult:
        """Полнотекстовый поиск с фильтрацией"""
        start_time = time.time()
        
        # Конструирование ESL запроса
        query = self._build_search_query(search_query)
        
        try:
            response = self.es.search(
                index=self.products_index,
                body={
                    "query": query,
                    "from": (search_query.page - 1) * search_query.page_size,
                    "size": search_query.page_size,
                    "sort": self._get_sort_order(search_query.sort_by),
                    "aggs": self._build_aggregations()
                }
            )
            
            took_ms = int((time.time() - start_time) * 1000)
            
            total = response["hits"]["total"]["value"]
            results = [hit["_source"] for hit in response["hits"]["hits"]]
            
            logger.info(f"✓ Поиск выполнен: {total} результатов за {took_ms}ms")
            
            return SearchResult(
                total=total,
                page=search_query.page,
                page_size=search_query.page_size,
                total_pages=(total + search_query.page_size - 1) // search_query.page_size,
                results=results,
                aggregations=response.get("aggregations"),
                took_ms=took_ms
            )
        
        except Exception as e:
            logger.error(f"✗ Ошибка поиска: {e}")
            raise
    
    def _build_search_query(self, search_query: SearchQuery) -> Dict[str, Any]:
        """Конструирование ES запроса"""
        query = {
            "bool": {
                "must": [],
                "filter": []
            }
        }
        
        # Основной текстовый поиск
        if search_query.query:
            query["bool"]["must"].append({
                "multi_match": {
                    "query": search_query.query,
                    "fields": ["name^3", "description^2", "search_text"],
                    "fuzziness": "AUTO",
                    "operator": "or"
                }
            })
        
        # Фильтр по категории
        if search_query.category_id:
            query["bool"]["filter"].append({
                "term": {"category_id": search_query.category_id}
            })
        
        # Фильтр по цене
        if search_query.min_price is not None or search_query.max_price is not None:
            price_filter = {}
            if search_query.min_price is not None:
                price_filter["gte"] = search_query.min_price
            if search_query.max_price is not None:
                price_filter["lte"] = search_query.max_price
            
            query["bool"]["filter"].append({"range": {"price": price_filter}})
        
        # Фильтр по рейтингу
        if search_query.min_rating is not None:
            query["bool"]["filter"].append({
                "range": {"rating": {"gte": search_query.min_rating}}
            })
        
        # Фильтр по наличию
        if search_query.in_stock:
            query["bool"]["filter"].append({
                "range": {"stock_quantity": {"gt": 0}}
            })
        
        # Фильтр по статусу
        query["bool"]["filter"].append({
            "term": {"status": "active"}
        })
        
        return query
    
    def _get_sort_order(self, sort_by: str) -> List[Dict[str, str]]:
        """Определение порядка сортировки"""
        sorts = {
            "relevance": [{"_score": {"order": "desc"}}, {"created_at": {"order": "desc"}}],
            "price_asc": [{"price": {"order": "asc"}}],
            "price_desc": [{"price": {"order": "desc"}}],
            "rating": [{"rating": {"order": "desc"}}, {"review_count": {"order": "desc"}}],
            "newest": [{"created_at": {"order": "desc"}}]
        }
        return sorts.get(sort_by, sorts["relevance"])
    
    def _build_aggregations(self) -> Dict[str, Any]:
        """Конструирование агрегаций"""
        return {
            "categories": {
                "terms": {"field": "category_name", "size": 100}
            },
            "brands": {
                "terms": {"field": "brand", "size": 50}
            },
            "price_ranges": {
                "range": {
                    "field": "price",
                    "ranges": [
                        {"to": 10000},
                        {"from": 10000, "to": 50000},
                        {"from": 50000, "to": 100000},
                        {"from": 100000}
                    ]
                }
            },
            "ratings": {
                "terms": {"field": "rating", "size": 5}
            }
        }
    
    def autocomplete(self, prefix: str, limit: int = 10) -> List[str]:
        """Автодополнение"""
        try:
            response = self.es.search(
                index=self.products_index,
                body={
                    "query": {
                        "match_phrase_prefix": {
                            "name": {
                                "query": prefix,
                                "boost": 2
                            }
                        }
                    },
                    "size": limit,
                    "_source": ["name"]
                }
            )
            
            suggestions = list(set(
                hit["_source"]["name"]
                for hit in response["hits"]["hits"]
            ))
            
            return sorted(suggestions)[:limit]
        
        except Exception as e:
            logger.error(f"Ошибка автодополнения: {e}")
            return []
