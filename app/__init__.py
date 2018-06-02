from flask import Flask
from app.album.views import album

app = Flask(__name__)

app.register_blueprint(album, url_prefix='/album')