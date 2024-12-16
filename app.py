from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from peewee import fn  # 集計のために使用
from models import Review, Product, Order

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
        .select(Product.name, fn.SUM(Review.review_count).alias('total_reviews'))
        .join(Product, on=(Review.product_id == Product.id))
        .group_by(Product.name)
        .order_by(fn.SUM(Review.review_count).desc())
    )

    # テンプレートで利用できるようにデータを準備
    items = [{"name": row.product.name, "review_count": row.total_reviews} for row in query]


    # 月別売上を集計
    monthly_sales = (
        Order
        .select(fn.strftime('%m', Order.order_date).alias('month'), fn.SUM(Product.price).alias('total_sales'))
        .join(Product)
        .group_by(fn.strftime('%m', Order.order_date))
        .order_by(fn.strftime('%m', Order.order_date))
    )

    # 月ごとの売上データを整形
    monthly_sales_data = [
        {"month": int(row.month), "total_sales": row.total_sales}
        for row in monthly_sales
    ]

    # 月のリストを作成（全月にデータがない場合に備える）
    months = list(range(1, 13))
    monthly_sales_dict = {entry["month"]: entry["total_sales"] for entry in monthly_sales_data}

    # 各月の売上を確実に初期化（売上がない月は0）
    monthly_sales_display = [
        {"month": month, "total_sales": monthly_sales_dict.get(month, 0)} for month in months
    ]



    return render_template("index.html", 
                           title="レビュー一覧", 
                           items=items,
                           monthly_sales=monthly_sales_display)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
