from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Configs
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='templates')
app.config.from_object(Configs)

db = SQLAlchemy()
db.init_app(app=app)

login_manager = LoginManager(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from mod_user.user import user
from mod_user.admin import admin

from mod_application.task import task
from mod_application.group import group

app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(group)
app.register_blueprint(task)


