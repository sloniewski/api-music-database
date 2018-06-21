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
    app.register_blueprint(album, url_prefix='/albums')
    app.register_blueprint(band, url_prefix='/bands')

    # register models
    db.init_app(app=app)

    return app
