from db import db


class UserModel(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String, unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String, unique=True, nullable=False)
