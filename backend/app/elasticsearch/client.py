from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from app.config import settings
from app.utils.logger import logger


class ElasticsearchClient:
    """Singleton для подключения к Elasticsearch"""
    
    _instance = None
    _client: Elasticsearch = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._connect()
    
    def _connect(self):
        """Инициализация подключения"""
        try:
            es_url = f"{settings.es_config.ELASTICSEARCH_SCHEME}://{settings.es_config.ELASTICSEARCH_HOST}:{settings.es_config.ELASTICSEARCH_PORT}"
            
            self._client = Elasticsearch(
                hosts=[es_url],
                timeout=settings.es_config.ELASTICSEARCH_TIMEOUT,
                max_retries=3,
                retry_on_timeout=True,
                verify_certs=False,  # Для development
                request_timeout=30
            )
            
            info = self._client.info()
            logger.info(f"✓ Elasticsearch {info['version']['number']} подключен")
            
        except ConnectionError as e:
            logger.error(f"✗ Ошибка подключения Elasticsearch: {e}")
            raise
    
    @property
    def client(self) -> Elasticsearch:
        if self._client is None:
            self._connect()
        return self._client
    
    def health_check(self) -> dict:
        """Проверка здоровья кластера"""
        try:
            return self._client.cluster.health()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise
    
    def close(self):
        """Закрытие подключения"""
        if self._client:
            self._client.close()
            self._client = None

# Глобальный экземпляр
es_client = ElasticsearchClient()
