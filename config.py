from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")
    USERNAME = os.environ.get("MYSQL_USER")
    PASSWORD = os.environ.get("MYSQL_PASSWORD")
    DATABASE = os.environ.get("MYSQL_DATABASE")

    SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@localhost/{2}".format(USERNAME, PASSWORD, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_TITLE = "Flask REST API"

    @staticmethod
    def init_app(app):
        pass