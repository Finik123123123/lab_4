from db import db


class BLOCKLIST(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jwi = db.Column(db.Integer)
