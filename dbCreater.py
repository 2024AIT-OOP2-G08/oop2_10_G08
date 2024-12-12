import random
import datetime
from faker import Faker
from peewee import *

# データベース設定
db = SqliteDatabase('createdDB.db')

# ベースモデル
class BaseModel(Model):
    class Meta:
        database = db

# モデル定義
class User(BaseModel):
    name = CharField()
    age = IntegerField()

class Product(BaseModel):
    name = CharField()
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = IntegerField(default=0)

class Review(BaseModel):
    user = ForeignKeyField(User, backref='reviews')
    product = ForeignKeyField(Product, backref='reviews')
    review_count = IntegerField()
    review_comment = TextField()

class Order(BaseModel):
    user = ForeignKeyField(User, backref='orders')
    product = ForeignKeyField(Product, backref='orders')
    order_date = DateTimeField(default=datetime.datetime.now)

# データベースの初期化
def initialize_database():
    with db:
        db.create_tables([User, Product, Review, Order])
    print("テーブルを作成しました。")

# データ生成と挿入
def generate_sample_data(record_count=500):
    fake = Faker("en")  # 日本語にしたければja_JPを指定
    users = []
    products = []

    # ユーザーを生成
    for _ in range(10):  # ユーザーは10人分
        user = User.create(name=fake.name(), age=random.randint(18, 60))
        users.append(user)

    # 商品を生成
    for _ in range(20):  # 商品は100種類
        product = Product.create(
            name=fake.word(),
            price=random.randint(1000, 50000),
            quantity=random.randint(0, 500)
        )
        products.append(product)

    # 注文とレビューを生成
    for _ in range(record_count):
        user = random.choice(users)
        product = random.choice(products)
        
        # 注文を作成
        Order.create(
            user=user,
            product=product,
            order_date=fake.date_time_this_year()
        )
        
        # レビューを作成（一定確率で）
        if random.random() < 0.7:  # 70%の確率でレビューを作成
            Review.create(
                user=user,
                product=product,
                review_count=random.randint(1, 5),
                review_comment=fake.sentence()
            )

    print(f"{record_count}件のデータを生成しました。")

# データ確認
def display_data():
    print("\nユーザーサンプル:")
    for user in User.select().limit(5):
        print(f"名前: {user.name}, 年齢: {user.age}")
    
    print("\n商品サンプル:")
    for product in Product.select().limit(5):
        print(f"商品名: {product.name}, 価格: {product.price}, 在庫: {product.quantity}")
    
    print("\n注文サンプル:")
    for order in Order.select().limit(5):
        print(f"注文ユーザー: {order.user.name}, 商品: {order.product.name}, 注文日: {order.order_date}")
    
    print("\nレビューサンプル:")
    for review in Review.select().limit(5):
        print(f"レビュー対象: {review.product.name}, ユーザー: {review.user.name}, コメント: {review.review_comment}")

# 実行例
if __name__ == "__main__":
    initialize_database()
    generate_sample_data(record_count=500)
    display_data()
