from .user import user_bp
from .product import product_bp
from .order import order_bp
from .inventoryManagement import inventoryManagement_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  product_bp,
  order_bp,
  inventoryManagement_bp
]
