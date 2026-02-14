from typing import Any, Dict


class ProductIndexConfig:    
    INDEX_NAME = "products"
    
    SETTINGS: Dict[str, Any] = {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "refresh_interval": "1s",
        "analysis": {
            "analyzer": {
                "russian_analyzer": {
                    "type": "standard",
                    "stopwords": "_russian_"
                }
            }
        }
    }
    
    MAPPINGS: Dict[str, Any] = {
        "properties": {
            "id": {"type": "integer"},
            "sku": {"type": "keyword"},
            "name": {
                "type": "text",
                "analyzer": "russian_analyzer",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "description": {"type": "text", "analyzer": "russian_analyzer"},
            "search_text": {"type": "text", "analyzer": "russian_analyzer"},
            "price": {"type": "scaled_float", "scaling_factor": 100},
            "discount_price": {"type": "scaled_float", "scaling_factor": 100},
            "stock_quantity": {"type": "integer"},
            "is_available": {"type": "boolean"},
            "is_active": {"type": "boolean"},
            "is_featured": {"type": "boolean"},
            "is_bestseller": {"type": "boolean"},
            "category_id": {"type": "integer"},
            "category_name": {"type": "keyword"},
            "average_rating": {"type": "scaled_float", "scaling_factor": 10},
            "review_count": {"type": "integer"},
            "popularity_score": {"type": "integer"},
            "sales_count": {"type": "integer"},
            "view_count": {"type": "integer"},
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"},
        }
    }
    
    @classmethod
    def get_mapping(cls) -> Dict[str, Any]:
        return {
            "settings": cls.SETTINGS,
            "mappings": cls.MAPPINGS
        }
