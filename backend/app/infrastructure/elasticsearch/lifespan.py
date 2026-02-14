from contextlib import asynccontextmanager
from fastapi import FastAPI
from elasticsearch.exceptions import TransportError
from app.infrastructure.elasticsearch.client import ElasticsearchClient, es_config
from backend.app.core.logger import get_logger

logger = get_logger() 

@asynccontextmanager
async def es_lifespan(app: FastAPI):
    es_client = ElasticsearchClient(config=es_config)
    
    logger.info("Подключение к Elasticsearch...")
    
    try:
        es = await es_client.connect()
        app.state.es_client = es
        logger.info("Подключение к Elasticsearch успешно.")
    except TransportError as e:
        logger.error(f"Ошибка подключения к Elasticsearch: {e}")
        raise 

    try: 
        yield
    except Exception as e:
        logger.error(f"Ошибка выполнения операции: {e}")
        raise e
    
    finally:
        try:
            await es_client.disconnect()
            logger.info("Сессия с Elasticsearch закрыта.")
        except Exception as e:
            logger.error(f"Ошибка при закрытии сессии с Elasticsearch: {e}")
