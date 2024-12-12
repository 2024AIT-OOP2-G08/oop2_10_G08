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

    query = (
        Review
        .select(Product.name, fn.SUM(Review.review_count).alias('total_reviews'))
        .join(Product, on=(Review.product_id == Product.id))
        .group_by(Product.name)
    )

    # テンプレートで利用できるようにデータを準備
    items = [{"name": row.product.name, "review_count": row.total_reviews} for row in query]

    return render_template("index.html", title="レビュー一覧", items=items)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
