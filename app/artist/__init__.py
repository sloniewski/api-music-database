from flask import Blueprint

artist = Blueprint('artist', __name__)

from . import views
