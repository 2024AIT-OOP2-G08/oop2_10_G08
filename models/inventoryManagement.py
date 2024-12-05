from peewee import Model, ForeignKeyField, IntegerField
from .db import db
from .product import Product  # Productモデルをインポート

class InventoryManagement(Model):
    product = ForeignKeyField(Product, backref='inventories')  # 製品名を外部キーとして関連付け
    quantity = IntegerField()  # 在庫の個数を保存

    class Meta:
        database = db