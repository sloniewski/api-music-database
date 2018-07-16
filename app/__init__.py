from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from app.config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # register blueprints
    from app.album import album
    from app.band import band
    from app.auth import auth
    from app.artist import artist
    app.register_blueprint(album, url_prefix='/albums')
    app.register_blueprint(band, url_prefix='/bands')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(artist, url_prefix='/artist')

    # register models
    db.init_app(app=app)
    # db.create_all(app=app)

    return app
