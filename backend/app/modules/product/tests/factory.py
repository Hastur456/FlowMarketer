from decimal import Decimal
from itertools import count
from uuid import UUID

from app.modules.product.domain.entities.product import Product


_sequence = count(1)


def make_product(
    *,
    category_id: UUID,
    name: str | None = None,
    slug: str | None = None,
    price: Decimal | str = Decimal("100.00"),
    stock_quantity: int = 10,
    is_active: bool = True,
    is_featured: bool = False,
    sku: str | None = None,
    **overrides,
) -> Product:
    number = next(_sequence)

    data = {
        "name": name or f"Product {number}",
        "slug": slug or f"product-{number}",
        "description": f"Description {number}",
        "category_id": category_id,
        "price": Decimal(price),
        "stock_quantity": stock_quantity,
        "is_active": is_active,
        "is_featured": is_featured,
        "sku": sku or f"SKU-{number}",
        "gallery_urls": [f"https://example.com/products/{number}.jpg"],
    }
    data.update(overrides)

    return Product(**data)
