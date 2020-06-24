from repositories.db import db


class Item(db.Document):
    name = db.StringField(required=True, unique=True)
    description = db.StringField(required=True)
    price = db.FloatField(required=True)
    supplier = db.StringField(required=True)
    category = db.StringField(required=True)