from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Configs
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='templates')
app.config.from_object(Configs)

db = SQLAlchemy()
db.init_app(app=app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

from mod_admin import admin
from mod_app import todo
from mod_user import user

app.register_blueprint(admin)
app.register_blueprint(todo)
app.register_blueprint(user)

