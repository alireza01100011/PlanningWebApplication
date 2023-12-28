from os import getenv

class Configs():
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')