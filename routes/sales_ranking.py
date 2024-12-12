from flask import Blueprint, render_template, request, redirect, url_for
from models import Product

# Blueprintの作成
sales_ranking_bp = Blueprint('sales_ranking', __name__, url_prefix='/sales_ranking')

@sales_ranking_bp.route('/')
def ranking():
    # 今月の売上を計算
    sales_data = []
    products = Product.select()
    
    for product in products:
        # 各製品の売上数と価格を取得
        quantity_sold = product.quantity
        price = product.price
        sales_amount = quantity_sold * price
        
        sales_data.append({
            'name': product.name,
            'quantity': quantity_sold,
            'price': price,
            'sales_amount': sales_amount
        })

    sales_data.sort(key=lambda x: x['sales_amount'], reverse=True)
    
    
    return render_template('ranking.html', 
                        title='製品別売上ダッシュボード',
                        sales_data=sales_data)