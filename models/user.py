from datetime import datetime
from factory import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    birthdate = db.Column(db.Datetime)
    created_at = db.Column(db.Datetime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User {self.username}>"