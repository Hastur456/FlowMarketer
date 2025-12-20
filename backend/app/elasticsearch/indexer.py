from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from app.elasticsearch.indices import PRODUCTS_INDEX_MAPPING, REVIEWS_INDEX_MAPPING
from typing import List, Dict, Any
from app.utils.logger import logger


class ElasticsearchIndexer:
    """Управление индексами и индексирование документов"""
    
    def __init__(self, es_client: Elasticsearch):
        self.es = es_client
        self.products_index = "products"
        self.reviews_index = "reviews"
    
    def create_indices(self) -> bool:
        """Создание всех индексов"""
        try:
            # Products индекс
            if not self.es.indices.exists(index=self.products_index):
                self.es.indices.create(
                    index=self.products_index,
                    body=PRODUCTS_INDEX_MAPPING
                )
                logger.info(f"✓ Индекс '{self.products_index}' создан")
            
            # Reviews индекс
            if not self.es.indices.exists(index=self.reviews_index):
                self.es.indices.create(
                    index=self.reviews_index,
                    body=REVIEWS_INDEX_MAPPING
                )
                logger.info(f"✓ Индекс '{self.reviews_index}' создан")
            
            return True
        except Exception as e:
            logger.error(f"✗ Ошибка создания индексов: {e}")
            raise
    
    def index_product(self, product_id: int, document: Dict[str, Any]) -> bool:
        """Индексирование одного продукта"""
        try:
            self.es.index(
                index=self.products_index,
                id=product_id,
                body=document
            )
            logger.debug(f"Продукт {product_id} индексирован")
            return True
        except Exception as e:
            logger.error(f"Ошибка индексирования продукта {product_id}: {e}")
            raise
    
    def bulk_index_products(self, products: List[Dict[str, Any]]) -> tuple[int, int]:
        """Массовое индексирование продуктов"""
        actions = [
            {
                "_index": self.products_index,
                "_id": product.get("id"),
                "_source": product
            }
            for product in products
        ]
        
        try:
            success, errors = bulk(
                self.es,
                actions,
                raise_on_error=False,
                chunk_size=500
            )
            
            if errors:
                logger.warning(f"Ошибок при индексировании: {len(errors)}")
            
            logger.info(f"✓ Индексировано {success} продуктов")
            return success, len(errors)
        
        except Exception as e:
            logger.error(f"Ошибка bulk индексирования: {e}")
            raise
    
    def update_product(self, product_id: int, partial_doc: Dict[str, Any]) -> bool:
        """Обновление продукта (partial update)"""
        try:
            self.es.update(
                index=self.products_index,
                id=product_id,
                body={"doc": partial_doc}
            )
            logger.debug(f"Продукт {product_id} обновлен в индексе")
            return True
        except Exception as e:
            logger.error(f"Ошибка обновления продукта {product_id}: {e}")
            raise
    
    def delete_product(self, product_id: int) -> bool:
        """Удаление продукта из индекса"""
        try:
            self.es.delete(index=self.products_index, id=product_id)
            logger.debug(f"Продукт {product_id} удален из индекса")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления продукта {product_id}: {e}")
            raise
    
    def refresh_indices(self) -> bool:
        """Обновление индексов для немедленной видимости"""
        try:
            self.es.indices.refresh(index=f"{self.products_index},{self.reviews_index}")
            logger.debug("Индексы обновлены")
            return True
        except Exception as e:
            logger.error(f"Ошибка обновления индексов: {e}")
            raise
    
    def delete_indices(self) -> bool:
        """Удаление всех индексов (для migration)"""
        try:
            for index in [self.products_index, self.reviews_index]:
                if self.es.indices.exists(index=index):
                    self.es.indices.delete(index=index)
                    logger.info(f"✓ Индекс '{index}' удален")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления индексов: {e}")
            raise
