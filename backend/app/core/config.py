"""
Конфигурация backend приложения
"""


import os
from typing import Union, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field, field_validator, computed_field
from dotenv import load_dotenv

load_dotenv()


class RunConfig(BaseModel):
    cors_origins: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    app_host: str = "localhost"
    app_port: str = 8000


class ElasticSearchConfig(BaseSettings):
    """Конфигурация Elasticsearch с валидацией для Pydantic v2."""
    
    model_config = SettingsConfigDict(
        env_prefix="ES_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Основные параметры подключения
    hosts: List[str] = Field(
        default=["http://localhost:9200"],
        description="Список хостов Elasticsearch"
    )
    
    # Аутентификация
    api_key: str | None = Field(default=None, description="API ключ для аутентификации")
    username: str | None = Field(default=None, alias="user")
    password: str | None = Field(default=None)
    
    # SSL/TLS
    verify_certs: bool = Field(default=False, description="Проверка SSL сертификатов")
    ca_certs: str | None = Field(default=None, description="Путь к CA сертификатам")
    ssl_show_warn: bool = Field(default=False)
    
    # Таймауты и retry
    request_timeout: int = Field(default=30, ge=1, le=300)
    max_retries: int = Field(default=3, ge=0, le=10)
    retry_on_timeout: bool = Field(default=True)
    
    # Connection pool
    max_connections: int = Field(default=10, ge=1, le=100)
    connections_per_node: int = Field(default=10, ge=1, le=50)
    
    # Индексы для интернет-магазина
    products_index: str = Field(default="products", description="Индекс товаров")
    orders_index: str = Field(default="orders", description="Индекс заказов")
    users_index: str = Field(default="users", description="Индекс пользователей")
    
    @field_validator("hosts", mode="before")
    @classmethod
    def parse_hosts(cls, v):
        """Парсинг хостов из строки или списка."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @computed_field
    @property
    def connection_config(self) -> dict:
        """Конфигурация подключения для AsyncElasticsearch."""
        config = {
            "hosts": self.hosts,
            "request_timeout": self.request_timeout,
            "max_retries": self.max_retries,
            "retry_on_timeout": self.retry_on_timeout,
            "verify_certs": self.verify_certs,
            "ssl_show_warn": self.ssl_show_warn,
            "connections_per_node": self.connections_per_node,
        }
        
        if self.api_key:
            config["api_key"] = self.api_key
        elif self.username and self.password:
            config["basic_auth"] = (self.username, self.password)
        
        if self.ca_certs:
            config["ca_certs"] = self.ca_certs
        
        return config



class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.getcwd(), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    DB_USER: str | None = Field(default=None, description="Database username")
    DB_PASSWORD: str | None = Field(default=None, description="Database password")
    DB_HOST: str | None = Field(default=None, description="Database host")
    DB_PORT: str | None = Field(default=None, description="Database port")
    DB_NAME: str | None = Field(default=None, description="Database name")

    TEST_DB_URL: str = "sqlite+aiosqlite:///:memory:"

    def get_url(self, test_mode: bool = False):
        if test_mode:
            return self.TEST_DB_URL
        
        if all([self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME, self.DB_PORT]):
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
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
