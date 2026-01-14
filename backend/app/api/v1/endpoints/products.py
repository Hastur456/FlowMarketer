from fastapi import APIRouter, FastAPI, Depends

from app.dependencies.es_depends import get_es_client, get_product_service
from app.elasticsearch.searchers.product_searcher import ProductSearcher

router = APIRouter(prefix="products")


@router.get("/search")
async def search_products(query: str, es_service: ProductSearcher=Depends(get_product_service)):
    hits = await es_service.search_by_text(query)

    return hits

