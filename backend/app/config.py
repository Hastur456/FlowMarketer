import os
from typing import Union, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field


class RunConfig(BaseModel):
    cors_origins: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    app_host: str = "localhost"
    apo_port: str = 8000


class ElasticSearchConfig(BaseModel):
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_SCHEME: str = "http"
    ELASTICSEARCH_TIMEOUT: int = 30

    # ELASTICSEARCH_URL: str = Field(default="https://es.example.com:9200")
    # ELASTICSEARCH_CA_CERTS: str = Field(default="/etc/ssl/certs/http_ca.crt")

    # # Рекомендуется API key (или basic_auth, если у вас так принято)
    # ELASTICSEARCH_API_KEY: str | None = None
    # ELASTICSEARCH_USER: str | None = None
    # ELASTICSEARCH_PASSWORD: str | None = None

    # ELASTICSEARCH_REQUEST_TIMEOUT: int = 10
    # ELASTICSEARCH_MAX_RETRIES: int = 5
    # ELASTICSEARCH_RETRY_ON_TIMEOUT: bool = True


class DatabaseConfig(BaseModel):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    DB_USER: str | None = Field(default=None, description="Database username")
    DB_PASSWORD: str | None = Field(default=None, description="Database password")
    DB_HOST: str | None = Field(default=None, description="Database host")
    DB_PORT: str | None = Field(default=None, description="Database port")
    DB_NAME: str | None = Field(default=None, description="Database name")

    TEST_DB_URL: str = "sqlite+aiosqlite:///:memory:"

    def get_url(self, test_mode: bool = True):
        if test_mode:
            return self.TEST_DB_URL
        
        if all([self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME, self.DB_PORT]):
            return "postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
        return self.TEST_DB_URL


class LoggerConfig(BaseModel):
    LOG_PATH: str = "debug.log"
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    es_config: ElasticSearchConfig = ElasticSearchConfig()
    logger_config: LoggerConfig = LoggerConfig()
    run: RunConfig = RunConfig()
    database: DatabaseConfig = DatabaseConfig()


settings = Settings()
database_url = settings.database.get_url()

