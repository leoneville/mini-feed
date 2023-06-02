# Validação da rota
from factory import api, jwt
from pydantic import BaseModel
from spectree import Response
from datetime import timedelta

# Blueprint e acesso aos dados da requisição
from flask import Blueprint, request

# Função para criar JWT token
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

# Modelo para buscarmos o usuário no banco de dados
from models import User

# Esquema com retorno de um campo "msg"
from utils.responses import DefaultResponse
from config import BLACKLIST


auth_controller = Blueprint("auth_controller", __name__, url_prefix="/auth")


class LoginMessage(BaseModel):
    username: str
    password: str


class LoginResponseMessage(BaseModel):
    access_token: str


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(header, payload):
    jti = payload["jti"]
    return jti in BLACKLIST


@auth_controller.post("/login")
@api.validate(json=LoginMessage, resp=Response(
    HTTP_200=LoginResponseMessage,
    HTTP_401=DefaultResponse), security={}, tags=["auth"])
def login():
    """
    Login in the system
    """
    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if user and user.verify_password(data["password"]):
        return {
            "access_token": "Bearer " + create_access_token(
                identity=user.username, expires_delta=timedelta(hours=3)
            )
        }, 200

    return {"msg": "Username or password do not match"}, 401


@auth_controller.post("/logout")
@api.validate(resp=Response(HTTP_200=DefaultResponse), tags=["auth"])
@jwt_required()
def logout():
    """
    Logout user
    """
    jti = get_jwt()["jti"]
    BLACKLIST.add(jti)
    return {"msg": "Logout successfully"}, 200
