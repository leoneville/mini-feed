from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")

    APP_TITLE = "Flask REST API"

    @staticmethod
    def init_app(app):
        pass