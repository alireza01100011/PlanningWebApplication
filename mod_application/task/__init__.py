from flask import Blueprint

from app import app

task = Blueprint('task', __name__,
                 url_prefix='/task/')

from .models import *
from .routes import *