from factory import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.UnicodeText, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"<Post {self.id}>"