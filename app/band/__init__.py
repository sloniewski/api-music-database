from flask import Blueprint

band = Blueprint('band', __name__)

from . import views
