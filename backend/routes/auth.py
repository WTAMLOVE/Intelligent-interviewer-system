from flask import request
from flask_restx import Namespace, Resource, fields
from extensions import db
from models.user import User
from services.user_service import create_user, authenticate_user
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

ns = Namespace("auth", description="用户认证")

user_model = ns.model(
    "User",
    {
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "role": fields.String(
            required=False, description="admin|interviewer|interviewee"
        ),
    },
)

login_model = ns.model(
    "Login",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)


@ns.route("/register")
class Register(Resource):
    @ns.expect(user_model)
    def post(self):
        data = request.json
        role = data.get("role", "interviewee")
        # basic validation
        if (
            not data.get("username")
            or not data.get("email")
            or not data.get("password")
        ):
            return {"message": "username, email and password are required"}, 400

        try:
            user = create_user(
                data["username"], data["email"], data["password"], role=role
            )
        except ValueError as e:
            return {"message": str(e)}, 400

        return {"message": "user created", "user": user.to_dict()}, 201


@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.json
        user = authenticate_user(data["username"], data["password"])
        if not user:
            # return a uniform message for any authentication failure
            return {"message": "用户名密码错误"}, 401
        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token, "user": user.to_dict()}, 200


@ns.route("/me")
class Me(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        # lightweight user info
        user = User.query.get(user_id)
        if not user:
            return {"message": "not found"}, 404
        return user.to_dict()
