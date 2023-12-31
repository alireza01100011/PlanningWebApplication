from sqlalchemy import Column, Integer, String, ForeignKey, Text
from datetime import datetime
from flask_login import UserMixin

from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, unique=True, primary_key=True)
    full_name = Column(String(128), unique=False, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), unique=False, nullable=False)
    roll = Column(Integer, default=0, unique=False)
    todos = db.relationship('Todo', backref='user')

    def __init__(self, full_name:str, email:str, password:str,
                 roll:int=0) -> None:
        
        self.full_name = full_name
        self.email = email
        self.password = password
        self.roll = roll

    def __repr__(self):
        return f'{__name__.__class__.__name__}< id:{self.id} - email:{self.email} - roll:{self.roll}>'
    
class Todo(db.Model):
    __tablename__ = 'todos'
    id = Column(Integer, unique=True, primary_key=True)
    tasks = Column(Text, unique=False, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)