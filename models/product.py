from peewee import Model, CharField, DecimalField, IntegerField
from .db import db

class Product(Model):
    name = CharField()
    price = DecimalField()
    quantity = IntegerField(default=0)  # デフォルト値を設定

    class Meta:
        database = db