from peewee import Model, ForeignKeyField, IntegerField
from .db import db
from order import Order 

class InventoryManagement(Model):
    product = ForeignKeyField(Order, backref='anagements')  # 製品名を外部キーとして関連付け
    quantity = IntegerField()  # 在庫の個数を保存
    class Meta:
        database = db