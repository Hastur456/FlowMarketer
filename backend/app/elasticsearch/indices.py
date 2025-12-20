# Маппинг для products индекса
PRODUCTS_INDEX_MAPPING = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "russian_analyzer": {
                    "type": "standard",
                    "stopwords": "_russian_"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "name": {
                "type": "text",
                "analyzer": "russian_analyzer",
                "fields": {
                    "keyword": {"type": "keyword"},
                    "suggest": {"type": "completion"}
                }
            },
            "description": {
                "type": "text",
                "analyzer": "russian_analyzer"
            },
            "price": {
                "type": "float"
            },
            "category_id": {
                "type": "integer"
            },
            "category_name": {
                "type": "keyword"
            },
            "sku": {
                "type": "keyword"
            },
            "stock_quantity": {
                "type": "integer"
            },
            "rating": {
                "type": "float"
            },
            "review_count": {
                "type": "integer"
            },
            "image_url": {
                "type": "keyword",
                "index": False
            },
            "brand": {
                "type": "keyword"
            },
            "tags": {
                "type": "keyword"
            },
            "popularity_score": {
                "type": "float"
            },
            "created_at": {
                "type": "date"
            },
            "updated_at": {
                "type": "date"
            },
            "status": {
                "type": "keyword"
            },
            "search_text": {
                "type": "text",
                "analyzer": "russian_analyzer"
            }
        }
    }
}

# Маппинг для reviews индекса
REVIEWS_INDEX_MAPPING = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "product_id": {"type": "integer"},
            "user_id": {"type": "integer"},
            "rating": {"type": "integer"},
            "title": {
                "type": "text",
                "analyzer": "russian_analyzer"
            },
            "content": {
                "type": "text",
                "analyzer": "russian_analyzer"
            },
            "helpful_count": {"type": "integer"},
            "created_at": {"type": "date"}
        }
    }
}
