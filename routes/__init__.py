from .user import user_bp
from .product import product_bp
from .order import order_bp
from .review import review_bp
from .inventory import inventory_bp
from .sales_ranking import sales_ranking_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  product_bp,
  order_bp,
  review_bp,
  inventory_bp,
  sales_ranking_bp
]
