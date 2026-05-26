import pytest
from datetime import datetime, UTC
from app.modules.product.infrastructure.search.product_mapper import (
    ProductMapper,
    ProductSource,
)


def test_to_es_document_basic():
    src = ProductSource(
        id="00000000-0000-0000-0000-000000000001",
        name="iPhone 15 Pro",
        description="Apple smartphone",
        sku="APL-IP15",
        price=1000,
        discount_price=900,
        stock_quantity=10,
        category_id="00000000-0000-0000-0000-000000000002",
        category_name="Smartphones",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    doc = ProductMapper.to_es_document(src)

    assert doc["id"] == "00000000-0000-0000-0000-000000000001"
    assert doc["price"] == 1000.0
    assert doc["discount_price"] == 900.0
    assert doc["is_available"] is True
    assert "iphone" in doc["search_text"]
    assert "smartphones" in doc["search_text"]


def test_is_available_false_when_out_of_stock():
    src = {
        "id": "00000000-0000-0000-0000-000000000002",
        "name": "Test",
        "price": 100,
        "stock_quantity": 0,
        "is_active": True,
        "category_id": "00000000-0000-0000-0000-000000000001",
        "category_name": "Cat",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }

    doc = ProductMapper.to_es_document(src)
    assert doc["is_available"] is False
