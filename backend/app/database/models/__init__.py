import pkgutil
import importlib
from app.database.models.base import Base
from app.database.models.user import User
from app.database.models.access_token import AccessToken
from app.database.models.cart import CartItem
from app.database.models.product import Product
from app.database.models.category import Category
from app.database.models.order_item import OrderItem
from app.database.models.order import Order, OrderStatus
from app.database.models.payment import Payment, PaymentMethod, PaymentStatus
from app.database.models.review import Review
from app.database.models.user_addres import UserAddress


__all__ = [
    "Base",
    "User",
    "AccessToken",
    "CartItem",
    "Product",
    "Category",
    "OrderItem",
    "Payment", 
    "PaymentMethod", 
    "PaymentStatus",
    "Order", "OrderStatus", "OrderItem",
    "Review",
    "UserAddress"
]

# # Автоматический поиск и импорт всех модулей в текущей директории
# for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
#     full_module_name = f"{__name__}.{module_name}"
#     module = importlib.import_module(full_module_name)
    
#     # Ищем все классы, наследующие BaseModel
#     for attr_name in dir(module):
#         attr = getattr(module, attr_name)
#         if (isinstance(attr, type) and 
#             issubclass(attr, Base) and 
#             attr is not Base):
            
#             # Добавляем в текущее пространство имен и в __all__
#             globals()[attr_name] = attr
#             if attr_name not in __all__:
#                 __all__.append(attr_name)
