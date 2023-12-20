from flask import Blueprint

from app import app

user = Blueprint('admin', __name__,
                  url_prefix='/admin/')

from .routes import *