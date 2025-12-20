from pydantic import BaseModel
from app.schemas.product import ProductResponse


class BaseMapper:
    @staticmethod
    def _normalize_text(text: str):
        return " ".join(text.lower().split())
    
    @staticmethod
    def _calculate_search_text(*parts) -> str:
        return " ".join(parts)


class ProductMapper(BaseMapper):
    @staticmethod
    def to_elasticsearch_document(cls, product, category, ratings):
        return {
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "category_id": category.id,
            "category_name": category.name,
            "search_text": cls._calculate_search_text(
                product.name,
                product.description
            ),
            "average_rating": ratings["average"],
            "review_count": ratings["count"]
        }
    
    @staticmethod
    def from_elasticsearch_hit(hit):
        source = hit["_source"]
        return ProductResponse(
            id=source["id"],
            name=source["name"],
            price=source["price"],
            category_id=source["category_id"],
            category_name=source["category_name"],
            stock=source["stock"],
            average_rating=source["average_rating"],
            review_count=source["review_count"]
        )
