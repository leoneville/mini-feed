from datetime import datetime
from typing import List

from pydantic import BaseModel

from factory import db
from utils.models import OrmBase

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    birthdate = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    

class UserCreate(BaseModel):
    username: str
    email: str
    birthdate: datetime = None

class UserResponse(OrmBase):
    username: str
    email: str
    birthdate: datetime = None
    created_at: datetime

class UserResponseList(BaseModel):
    __root__: List[UserResponse]