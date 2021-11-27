import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
import sqlalchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "revolia"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .home import homePage
    from .auth import authPage

    app.register_blueprint(homePage, url_prefix = "/")
    app.register_blueprint(authPage, url_prefix = "/")

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "authPage.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))    

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app = app)
        print("Database Created.")