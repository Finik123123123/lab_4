from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    description =db.Column(db.String)
    price=db.Column(db.Float(precision=True),nullable=False,unique=False)
    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"),unique=False,nullable=False)
    store=db.relationship("StoreModel",back_populates="items")
    tag=db.relationship("Tagmodel",back_populates=True)
