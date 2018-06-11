from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .config import config
from .album import album
from .band import band

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(album, url_prefix='/albums')
    app.register_blueprint(band, url_prefix='/bands')
    return app
