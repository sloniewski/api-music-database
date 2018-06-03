from flask import Flask
from app.album.views import album
from app.band.views import band

app = Flask(__name__)

app.register_blueprint(album, url_prefix='/albums')
app.register_blueprint(band, url_prefix='/bands')