import unittest


from flask import Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy


from _models import Todo
from user import User


class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///test_datebase.db"
    TESTING = True


    def setUp(cls):

        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.db = SQLAlchemy()
        cls.db.init_app(app=cls.app)
        cls.db.create_all()

    def tearDown(cls):

        cls.db.session.remove()
        cls.db.drop_all()

    def test_CreateUser(self):
        print('Testing Create User')
        new_user = User()
        new_user.full_name = 'alireza'
        new_user.email = 'test@test.com'
        new_user.password = 'alireza'
        
        self.db.session.add(new_user)
        self.db.session.commit()


if __name__ == '__main__':
    unittest.main()    
