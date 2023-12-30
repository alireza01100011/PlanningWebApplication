from os import getenv, urandom

class Configs():
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = urandom(64)