from app.modules.product.application.dto import ProductCreateDTO
from app.modules.product.domain.entities.product import Product


class ProductApplicationMapper:
    @staticmethod
    def create_dto_to_domain(dto: ProductCreateDTO) -> Product:
        return Product(**dto.model_dump())
