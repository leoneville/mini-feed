from datetime import datetime
from typing import List

from factory import db
from pydantic import BaseModel

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.UnicodeText, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"<Post {self.id}>"
    

class PostCreate(BaseModel):
    text: str

class PostResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    author_id: int

    class Config:
        orm_mode = True

class PostResponseList(BaseModel):
    page: int
    pages: int
    total: int
    posts: List[PostResponse]