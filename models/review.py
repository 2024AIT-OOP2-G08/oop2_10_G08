from peewee import Model, ForeignKeyField, DateTimeField, IntegerField, CharField
from .db import db
from .user import User
from .product import Product

class Review(Model):
    user = ForeignKeyField(User, backref='reviews')
    product = ForeignKeyField(Product, backref='reviews')
    review_count = IntegerField()
    review_comment = CharField()

    class Meta:
        database = db
