from os import getenv, urandom

class Configs():
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = '123as1df321sad32f1as32df132as1df'
    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_PORT = getenv('MAIL_PORT')
    REDIS_SERVER_URL = getenv('REDIS_SERVER_URL')