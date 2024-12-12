from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from models import Product

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
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
    
    return render_template('index.html', 
                         title='製品別売上ダッシュボード',
                         sales_data=sales_data)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
