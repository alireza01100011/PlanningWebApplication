from sqlalchemy import Column, Integer, String, ForeignKey, Text
from datetime import datetime
from flask_login import UserMixin

from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, unique=True, primary_key=True)
    full_name = Column(String(128), unique=False, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), unique=False, nullable=False)
    roll = Column(Integer, default=0, unique=False)
    todos = db.relationship('Todo', backref='user')

class Todo(db.Model):
    __tablename__ = 'todos'
    id = Column(Integer, unique=True, primary_key=True)
    tasks = Column(Text, unique=False, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)