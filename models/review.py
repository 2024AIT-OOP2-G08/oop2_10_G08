from peewee import Model, ForeignKeyField, TextField, IntegerField
from .db import db
from .user import User
from .product import Product

class Review(Model):
    user = ForeignKeyField(User, backref='reviews')
    product = ForeignKeyField(Product, backref='reviews')
    review_count = IntegerField()  # int
    review_comment = TextField()  # str

    class Meta:
        database = db