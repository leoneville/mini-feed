from datetime import datetime

from factory import api, db
from flask import Blueprint, jsonify
from flask.globals import request
from spectree import Response

from models import User

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")

@user_controller.get("/<int:user_id>")
@api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_500=None), tags=["users"])
def get_user(user_id):
    """
    Get a specified user
    """
    try:
        user = db.session.get(User, user_id)

        if user is None:
            return {"msg": f"There is no user with id {user_id}"}, 404
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "birthdate": user.birthdate.isoformat() if user.birthdate else None,
            "created_at": user.created_at.isoformat(),
        }, 200
    except Exception as error:
        print(f"<get_user: {type(error)}>")
        return {"msg": "Ops! Something went wrong."}, 500


@user_controller.get("/")
@api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_500=None), tags=["users"])
def get_users():
    """
    Get all users
    """
    try:
        users = User.query.all()

        if len(users) == 0:
            return {"msg": "no registered user"}, 404

        return jsonify(
            [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "birthdate": user.birthdate.isoformat() if user.birthdate else None,
                    "created_at": user.created_at.isoformat()
                }
                for user in users
            ]
        ), 200
    except Exception as error:
        print(f"<get_users: {type(error)}>")
        return {"msg": "Ops! Something went wrong."}, 500

@user_controller.post("/")
@api.validate(resp=Response(HTTP_201=None, HTTP_400=None, HTTP_409=None, HTTP_500=None), tags=["users"])
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
        
        user = User(
            username=data["username"], 
            email=data["email"],
            birthdate=datetime.fromisoformat(data["birthdate"]) if "birthdate" in data else None,
        )
        db.session.add(user)
        db.session.commit()

        return {"msg": "User created successfully"}, 201
    except KeyError:
        return {"msg": "username and email fields are required"}, 400
    except Exception as error:
        db.session.rollback()
        print(f"<create_user: {type(error)}>")
        return {"msg": "Ops! Something went wrong."}, 500



@user_controller.put("/<int:user_id>")
@api.validate(resp=Response(HTTP_200=None, HTTP_400=None, HTTP_404=None, HTTP_500=None), tags=["users"])
def put_user(user_id):
    """
    Update an user
    """
    try:
        user = db.session.get(User, user_id)

        if user is None:
            return {"msg": f"There is no user with id {user_id}"}, 404

        data = request.json

        user.username = data["username"]
        user.email = data["email"]
        if "birthdate" in data:
            user.birthdate = datetime.fromisoformat(data["birthdate"])

        db.session.commit()

        return {"msg": "User was updated"}, 200
    except KeyError:
        return {"msg": "username and email fields are required"}, 400
    except Exception as error:
        db.session.rollback()
        print(f"<put_user: {type(error)}>")
        return {"msg": "Ops! Something went wrong."}, 500


@user_controller.delete("/<int:user_id>")
@api.validate(resp=Response(HTTP_200=None, HTTP_404=None, HTTP_500=None), tags=["users"])
def delete_user(user_id):
    """
    Delete an user
    """
    try:
        user = db.session.get(User, user_id)

        if user is None:
            return {"msg": f"There is no user with id {user_id}"}, 404
        
        db.session.delete(user)
        db.session.commit()

        return {"msg": "User deleted from the database."}, 200
    except Exception as error:
        db.session.rollback()
        print(f"<delete_user: {type(error)}>")
        return {"msg": "Ops! Something went wrong."}, 500