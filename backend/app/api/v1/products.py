from fastapi import APIRouter, FastAPI, Depends

from backend.app.infrastructure.elasticsearch.es_depends import get_es_client
from backend.app.modules.product.infrastructure.search.product_searcher import ProductSearcher
from backend.app.modules.product.application.services.product_service import ProductService

router = APIRouter(prefix="products")


@router.get("/search")
async def search_products(query: str, es_service: ProductSearcher=Depends(get_product_service)):
    hits = await es_service.search_by_text(query)

    return hits
