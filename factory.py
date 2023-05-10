from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/')
    def hello_world():
        return "<h1>Hello World</h1>"
    
    return app
