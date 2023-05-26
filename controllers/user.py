from datetime import datetime
import json

from flask import Blueprint, jsonify
from flask.globals import request
from spectree import Response
from flask_jwt_extended import jwt_required, current_user
from factory import api, db

from models import User, UserCreate, UserEdit
from models.user import UserResponseList, UserResponse
from utils.responses import DefaultResponse

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")


@user_controller.get("/me")
@api.validate(resp=Response(HTTP_200=UserResponse), tags=["users"])
@jwt_required()
def get_current_user():
    """Returns information about the current user"""
    response = UserResponse.from_orm(current_user).json()

    return json.loads(response), 200


@user_controller.get("/<int:user_id>")
@api.validate(resp=Response(
    HTTP_200=UserResponse,
    HTTP_404=DefaultResponse,
    HTTP_500=DefaultResponse), tags=["users"])
@jwt_required()
def get_user(user_id):
    """
    Get a specified user
    """
    try:
        user = db.session.get(User, user_id)

        if user is None:
            return {"msg": f"There is no user with id {user_id}"}, 404

        response = UserResponse.from_orm(user).json()

        return json.loads(response), 200
    except Exception as error:
        print(f"<get_user: {type(error)}> - {error}")
        return {"msg": "Ops! Something went wrong."}, 500


@user_controller.get("/")
@api.validate(resp=Response(
    HTTP_200=UserResponseList,
    HTTP_500=DefaultResponse), tags=["users"])
@jwt_required()
def get_users():
    """
    Get all users
    """
    try:
        users = User.query.all()

        response = UserResponseList(
            __root__=[UserResponse.from_orm(user).dict() for user in users]
        ).json()

        return jsonify(json.loads(response)), 200
    except Exception as error:
        print(f"<get_users: {type(error)}> - {error}>")
        return {"msg": "Ops! Something went wrong."}, 500


@user_controller.post("/")
@api.validate(json=UserCreate, resp=Response(
    HTTP_201=DefaultResponse,
    HTTP_400=DefaultResponse,
    HTTP_409=DefaultResponse,
    HTTP_500=DefaultResponse), security={}, tags=["users"])
def create_user():
    """
    Create an user
    """
    try:
        data = request.json

        if User.query.filter_by(username=data["username"]).first():
            return {"msg": "username not available"}, 409

        if User.query.filter_by(email=data["email"]).first():
            return {"msg": "email not available"}, 409

        if "birthdate" in data:
            if data["birthdate"].endswith("Z"):
                data["birthdate"] = data["birthdate"][:-1]

        user = User(
            username=data["username"],
            email=data["email"],
            birthdate=datetime.fromisoformat(
                data["birthdate"]) if "birthdate" in data else None,
            password=data["password"],
        )
        db.session.add(user)
        db.session.commit()

        return {"msg": "User created successfully"}, 201
    except KeyError:
        return {"msg": "username and email fields are required"}, 400
    except Exception as error:
        db.session.rollback()
        print(f"<create_user: {type(error)}> - {error}>")
        return {"msg": "Ops! Something went wrong."}, 500


@user_controller.put("/")
@api.validate(json=UserEdit, resp=Response(
    HTTP_200=DefaultResponse,
    HTTP_400=DefaultResponse,
    HTTP_500=DefaultResponse), tags=["users"])
@jwt_required()
def put_user():
    """
    Update an user
    """
    try:
        user = current_user

        data = request.json

        valid_user = user.query.filter_by(username=data["username"]).first()

        if valid_user and valid_user.username != user.username:
            return {"msg": "username not available"}, 409

        if "birthdate" in data:
            if data["birthdate"].endswith("Z"):
                data["birthdate"] = data["birthdate"][:-1]
            user.birthdate = datetime.fromisoformat(data["birthdate"])

        user.username = data["username"]
        user.email = data["email"]

        db.session.commit()

        return {"msg": "User was updated"}, 200
    except KeyError:
        return {"msg": "username and email fields are required"}, 400
    except Exception as error:
        db.session.rollback()
        print(f"<put_user: {type(error)}> - {error}>")
        return {"msg": "Ops! Something went wrong."}, 500


@user_controller.delete("/")
@api.validate(resp=Response(
    HTTP_200=DefaultResponse,
    HTTP_404=DefaultResponse,
    HTTP_500=DefaultResponse), tags=["users"])
@jwt_required()
def delete_user():
    """
    Delete an user
    """
    try:
        user = current_user

        db.session.delete(user)
        db.session.commit()

        return {"msg": "User deleted from the database."}, 200
    except Exception as error:
        db.session.rollback()
        print(f"<delete_user: {type(error)}> - {error}>")
        return {"msg": "Ops! Something went wrong."}, 500
