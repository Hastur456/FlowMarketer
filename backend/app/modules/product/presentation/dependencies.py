from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from app.core.logger import logger
from app.infrastructure.elasticsearch.es_depends import get_es_client
from app.modules.product.application.services import ProductService
from app.modules.product.infrastructure.persistence import SqlAlchemyProductRepository
from app.modules.product.infrastructure.search.product_indexer import ProductIndexer
from app.modules.product.infrastructure.search.product_searcher import ProductSearcher


async def get_product_service(
    es_client: AsyncElasticsearch = Depends(get_es_client),
) -> ProductService:
    repository = SqlAlchemyProductRepository()
    indexer = ProductIndexer(es_client, logger)
    searcher = ProductSearcher(es_client, logger)
    return ProductService(
        repository=repository,
        indexer=indexer,
        searcher=searcher,
        logger=logger,
    )
