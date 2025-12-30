import pytest
from unittest.mock import AsyncMock, MagicMock
from app.elasticsearch.indexers.product_indexer import ProductIndexer


@pytest.mark.asyncio
async def test_create_index_when_not_exists():
    es = AsyncMock()
    es.indices.exists.return_value = False
    es.indices.create.return_value = {}

    logger = MagicMock()
    indexer = ProductIndexer(es, logger)

    result = await indexer.create_index()

    assert result is True
    es.indices.create.assert_called_once()


@pytest.mark.asyncio
async def test_index_one():
    es = AsyncMock()
    logger = MagicMock()

    indexer = ProductIndexer(es, logger)

    product = {
        "id": 1,
        "name": "Test",
        "price": 100,
        "stock_quantity": 5,
        "is_active": True,
        "category_id": 1,
        "category_name": "Cat",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }

    result = await indexer.index_one(product)

    assert result is True
    es.index.assert_called_once()


@pytest.mark.asyncio
async def test_delete_one():
    es = AsyncMock()
    logger = MagicMock()

    indexer = ProductIndexer(es, logger)
    result = await indexer.delete_one(42)

    assert result is True
    es.delete.assert_called_once_with(
        index=indexer.index_name,
        id=42,
        refresh=False,
    )
