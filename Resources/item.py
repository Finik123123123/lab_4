from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from Models import ItemModel
from Resources.schemas import PlainItemSchema, ItemUpdateSchema
from db import db

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, PlainItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwti=get_jwt()
        if not jwti.get("is_admin"):
            abort(401,message="Admin only")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Deleted!"}

    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, PlainItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(PlainItemSchema)
    @blp.response(200, PlainItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "Error occured")

        return item
