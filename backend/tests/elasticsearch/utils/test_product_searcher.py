import pytest
from unittest.mock import AsyncMock, MagicMock
from app.elasticsearch.searchers.product_searcher import ProductSearcher
from tests.elasticsearch.factories.product_es import product_es_hit


@pytest.mark.asyncio
async def test_search_by_text():
    es = AsyncMock()
    logger = MagicMock()

    es.search.return_value = {
        "hits": {
            "hits": [
                product_es_hit(**{"id": 1, "name": "iPhone", "price": 1000})
            ]
        }
    }

    searcher = ProductSearcher(es, logger)
    results = await searcher.search_by_text("iphone")

    es.search.assert_called_once()
    assert len(results) == 1
    assert results[0].id == 1
    assert results[0].name == "iPhone"


@pytest.mark.asyncio
async def test_filter_by_category():
    es = AsyncMock()
    logger = MagicMock()

    es.search.return_value = {"hits": {"hits": []}}

    searcher = ProductSearcher(es, logger)
    results = await searcher.filter_by_category(category_id=10)

    es.search.assert_called_once()
    assert results == []


@pytest.mark.asyncio
async def test_autocomplete():
    es = AsyncMock()
    logger = MagicMock()

    es.search.return_value = {
        "hits": {
            "hits": [
                {"_source": {"name": "iPhone 15"}},
                {"_source": {"name": "iPhone 14"}},
            ]
        }
    }

    searcher = ProductSearcher(es, logger)
    result = await searcher.autocomplete("iph")

    assert result == ["iPhone 15", "iPhone 14"]
