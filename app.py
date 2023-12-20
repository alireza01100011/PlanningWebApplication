from flask import Flask

app = Flask(__name__)

from mod_admin import admin
from mod_app import todo
from mod_user import user

app.register_blueprint(admin)
app.register_blueprint(todo)
app.register_blueprint(user)

