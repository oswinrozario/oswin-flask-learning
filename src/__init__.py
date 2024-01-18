from flask import Flask
import os
from src.controllers.auth import auth
from src.controllers.bookmarks import bookmarks
from src.service.db import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'default_secret_key'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///bookmarks.db')
        )
    else:
        app.config.from_mapping(test_config)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app
