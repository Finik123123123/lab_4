from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
import Models
import secrets
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from db import db
from Resources.item import blp as ItemBlueprint
from Resources.store import blp as StoreBlueprint
from Resources.tag import blp as TagBlueprint
from Resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)

    app.config["JMT_SECRET_KEY"] = "287965223752430890455601774923941826826"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token = BLOCKLIST.query.filter_by(jwi=jti).first()
        return token

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token has been revoked", "error": "token_revoked"}), 401

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Verification failed", "error": "invalid token"}), 401

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
