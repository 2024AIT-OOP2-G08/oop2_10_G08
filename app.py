from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from peewee import fn  # 集計のために使用
from models import Review, User, Product
from datetime import datetime

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
    
#     return render_template('index.html', 
#                          title='製品別売上ダッシュボード',
#                          sales_data=sales_data)


    # 製品ごとにレビュー数を集計
    query = (
        Review
        .select(Product.name, fn.AVG(Review.review_count).alias('total_reviews'))
        .join(Product, on=(Review.product_id == Product.id))
        .group_by(Product.name)
        .order_by(fn.AVG(Review.review_count).desc())
    )

    # テンプレートで利用できるようにデータを準備
    items = [{"name": row.product.name, "review_count": row.total_reviews} for row in query]

    return render_template("index.html", title="レビュー一覧", items=items)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
