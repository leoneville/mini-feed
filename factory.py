from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from models import User
    migrate.init_app(app, db)

    from controllers import user_controller
    app.register_blueprint(user_controller)
    
    return app
