from fastapi import APIRouter, Depends

from app.modules.product.application.services import ProductService
from app.modules.product.presentation.dependencies import get_product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/search")
async def search_products(
    query: str,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.search_products(query=query)
