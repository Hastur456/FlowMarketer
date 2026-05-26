import json
from typing import Any

from app.modules.product.domain.entities.product import Product
from app.modules.product.infrastructure.persistence.product_model import ProductModel


class ProductMapper:
    @staticmethod
    def to_domain(model: ProductModel) -> Product:
        return Product(
            id=model.id,
            name=model.name,
            slug=model.slug,
            description=model.description,
            category_id=model.category_id,
            price=model.price,
            discount_price=model.discount_price,
            cost_price=model.cost_price,
            stock_quantity=model.stock_quantity,
            reserved_stock=model.reserved_stock,
            sku=model.sku,
            meta_title=model.meta_title,
            meta_description=model.meta_description,
            tags=model.tags,
            image_url=model.image_url,
            gallery_urls=ProductMapper._loads_gallery_urls(model.gallery_urls),
            average_rating=model.average_rating,
            review_count=model.review_count,
            is_active=model.is_active,
            is_featured=model.is_featured,
            is_bestseller=model.is_bestseller,
            popularity_score=model.popularity_score,
            sales_count=model.sales_count,
            view_count=model.view_count,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(product: Product) -> ProductModel:
        data = ProductMapper.to_persistence_dict(product)
        return ProductModel(**data)

    @staticmethod
    def update_model(model: ProductModel, updates: Product | dict[str, Any]) -> ProductModel:
        data = (
            ProductMapper.to_persistence_dict(updates)
            if isinstance(updates, Product)
            else ProductMapper._normalize_persistence_dict(updates)
        )

        for field, value in data.items():
            if hasattr(model, field):
                setattr(model, field, value)

        return model

    @staticmethod
    def to_persistence_dict(product: Product) -> dict[str, Any]:
        data = product.model_dump(exclude={"created_at", "updated_at"}, exclude_none=True)
        return ProductMapper._normalize_persistence_dict(data)

    @staticmethod
    def _normalize_persistence_dict(data: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(data)

        if "gallery_urls" in normalized:
            normalized["gallery_urls"] = ProductMapper._dumps_gallery_urls(
                normalized["gallery_urls"]
            )

        return normalized

    @staticmethod
    def _loads_gallery_urls(value: str | None) -> list[str] | None:
        if not value:
            return None

        try:
            loaded = json.loads(value)
        except json.JSONDecodeError:
            return [url.strip() for url in value.splitlines() if url.strip()]

        return loaded if isinstance(loaded, list) else None

    @staticmethod
    def _dumps_gallery_urls(value: list[str] | str | None) -> str | None:
        if value is None or isinstance(value, str):
            return value

        return json.dumps(value)
