from flask import Blueprint

group = Blueprint('group', __name__, url_prefix='/group/')

from .routes import *