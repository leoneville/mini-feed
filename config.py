from dotenv import load_dotenv
import os

load_dotenv()

BLACKLIST = set()


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")
    USERNAME = os.environ.get("MYSQL_USER")
    PASSWORD = os.environ.get("MYSQL_PASSWORD")
    DATABASE_URL = os.environ.get("MYSQL_DATABASE_URL")
    DATABASE = os.environ.get("MYSQL_DATABASE")

    SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}".format(
        USERNAME, PASSWORD, DATABASE_URL, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_TITLE = "Flask REST API"

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_TOKEN_LOCATION = ["headers"]

    @staticmethod
    def init_app(app):
        pass
