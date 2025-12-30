from datetime import datetime, UTC


def product_es_hit(**overrides):
    base = {
        "_source": {
            "id": 1,
            "sku": "SKU-1",
            "name": "iPhone",
            "description": "Apple smartphone",
            "search_text": "iphone apple smartphone electronics",
            "price": 1000.0,
            "discount_price": None,
            "stock_quantity": 10,
            "is_available": True,
            "is_active": True,
            "is_featured": False,
            "is_bestseller": False,
            "category_id": 2,
            "category_name": "Smartphones",
            "average_rating": 4.8,
            "review_count": 120,
            "popularity_score": 100,
            "sales_count": 500,
            "view_count": 10000,
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat(),
        }
    }

    base["_source"].update(overrides)
    return base
