import jwt
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask_smorest import Blueprint
from flask_smorest import abort
from Models.user import UserModel
from blocklist import BLOCKLIST
from db import db
from sqlalchemy.exc import SQLAlchemyError
from schemas import UserSchema
from passlib.hash import pbkdf2_sha256

blp = Blueprint("Users", "user", description="Op on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="User exists")
        user = UserModel(username=user_data["username"], password=pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(user)
        db.session.commit()
        return {"message": "User created!"}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Deleted"}


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(401, message="Invalid")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required
    def post(self):
        jti = get_jwt()["jti"]
        block = BLOCKLIST(jwi=jti)
        try:
            db.session.add(block)
            db.session.commit()
        except SQLAlchemyError:
            abort(505)
        return {"message": "Logged out"}
