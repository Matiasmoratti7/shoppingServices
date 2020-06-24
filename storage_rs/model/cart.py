from repositories.db import db


class Cart(db.Document):
    username = db.StringField()
    status = db.StringField(required=True)
    items = db.ListField(db.ReferenceField('Item'))
    payment_method = db.StringField()
    total_amount = db.FloatField()