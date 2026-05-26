import pytest
from unittest.mock import AsyncMock, MagicMock
from app.modules.product.infrastructure.search.product_indexer import ProductIndexer


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
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "Test",
        "price": 100,
        "stock_quantity": 5,
        "is_active": True,
        "category_id": "00000000-0000-0000-0000-000000000002",
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
    product_id = "00000000-0000-0000-0000-000000000042"
    result = await indexer.delete_one(product_id)

    assert result is True
    es.delete.assert_called_once_with(
        index=indexer.index_name,
        id=product_id,
        refresh=False,
    )
