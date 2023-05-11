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