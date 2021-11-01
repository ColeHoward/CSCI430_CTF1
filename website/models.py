from .databases import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # alternative_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    balance = db.Column(db.Integer)
    action_type = db.Column(db.String(10))
    is_authenticated = db.Column(db.Boolean)

    def __str__(self):
        return "user:" + " " + self.username + " " + self.password

    # def get_id(self):
        # return str(self.alternative_id)