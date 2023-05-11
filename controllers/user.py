from datetime import datetime

from factory import db
from flask import Blueprint, jsonify
from flask.globals import request
from models import User

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")

@user_controller.get("/<int:user_id>")
def get_user(user_id):
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

@user_controller.get("/")
def get_users():
    users = User.query.all()

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

@user_controller.post("/")
def create_user():
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

@user_controller.put("/<int:user_id>")
def put_user(user_id):
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

@user_controller.delete("/<int:user_id>")
def delete_user(user_id):
    user = db.session.get(User, user_id)

    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404
    
    db.session.delete(user)
    db.session.commit()

    return {"msg": "User deleted from the database."}, 200