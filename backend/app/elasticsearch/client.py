"""Асинхронный клиент Elasticsearch."""

from typing import Optional
from elasticsearch import AsyncElasticsearch
from app.config import settings

es_config = settings.es_config


class ESClient:
    """Singleton для асинхронной работы с Elasticsearch."""
    
    _instance: AsyncElasticsearch|None = None
    
    @classmethod
    async def get_client(cls) -> AsyncElasticsearch:
        """Получить или создать async клиент."""
        if cls._instance is None:
            cls._instance = AsyncElasticsearch(
                hosts=[es_config.ELASTICSEARCH_HOST],
                verify_certs=False,
                ssl_show_warn=False,
            )
        return cls._instance
    
    @classmethod
    async def close(cls) -> None:
        """Закрыть соединение."""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
