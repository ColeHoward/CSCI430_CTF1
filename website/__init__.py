# this file makes 'websites' a python package... meaning we can import it
from datetime import datetime, timedelta
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from os import path
import sys
#  from app import logout
from .databases import db
from flask_login import LoginManager

DB_NAME = "database.db"


# initialize app
def create_app():
    app = Flask(__name__)
    # encrypt session data
    app.config['SECRET_KEY'] = ']TZ6kf8E9VV{~jCeTu~.]nZytGamY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    app.config.update(
        # SESSION_COOKIE_SECURE=True,
        # SESSION_COOKIE_HTTPONLY=True,
        # REMEMBER_COOKIE_DURATION=timedelta(minutes=25),
        # PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    )
    db.init_app(app)

    from website.models import User
    create_database(app)

    # ensure user not logged in is directed to login page onload
    # login_manager = LoginManager()
    # login_manager.login_view = 'login'
    # login_manager.session_protection = "strong"
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(id)
    #     # return User.query.filter_by(alternative_id=id).first()
    print('finished init')
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('database created!')
