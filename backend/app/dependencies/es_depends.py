from fastapi import Depends, Request
from elasticsearch import AsyncElasticsearch
from logging import Logger

from app.services.product_service import ProductService
from backend.app.utils.logger import get_logger


async def get_es_client(request: Request):
    return request.app.state.es_client


def get_product_service(
    es: AsyncElasticsearch = Depends(get_es_client),
    logger: Logger = Depends(get_logger),
) -> ProductService:
    return ProductService(es, logger)
