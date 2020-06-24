from repositories.db import db
import flask_bcrypt


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    role = db.StringField(required=True)

    def hash_password(self):
        pwd_hash = flask_bcrypt.generate_password_hash(self.password)
        self.password = pwd_hash.decode('utf8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)