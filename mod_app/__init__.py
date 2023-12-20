from flask import Blueprint

from app import app

todo = Blueprint('todo', __name__,
                 url_prefix='/')

from .routes import *