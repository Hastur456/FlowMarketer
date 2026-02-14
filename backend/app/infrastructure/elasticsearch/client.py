from typing import Optional
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError, TransportError
from backend.app.core.config import settings, ElasticSearchConfig


es_config = settings.es_config


class ElasticsearchClient:
    def __init__(self, config: ElasticSearchConfig):
        self.config = config
        self._client: Optional[AsyncElasticsearch] = None

    async def connect(self) -> AsyncElasticsearch:
        if self._client is None:
            try:
                self._client = AsyncElasticsearch(**self.config.connection_config)
                info = await self._client.info()
                es_version = info.get("version", {}).get("number", "unknown")
                cluster_name = info.get("cluster_name", "unknown")
                print(f"[Elasticsearch] Connected to {cluster_name} (v{es_version})")
            except (ConnectionError, TransportError) as e:
                print(f"[Elasticsearch] Connection failed: {e}")
                raise
        return self._client

    async def disconnect(self) -> None:
        if self._client is not None:
            try:
                await self._client.close()
                print("[Elasticsearch] Connection closed")
            except Exception as e:
                print(f"[Elasticsearch] Error during disconnect: {e}")
            finally:
                self._client = None

    async def health_check(self) -> bool:
        try:
            if self._client is None:
                return False
            health = await self._client.cluster.health()
            status = health.get("status")
            return status in ["green", "yellow"]
        except Exception:
            return False

    @property
    def client(self) -> AsyncElasticsearch:
        if self._client is None:
            raise RuntimeError("Elasticsearch client not connected. Call connect() first.")
        return self._client
