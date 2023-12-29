import re

from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField)
from wtforms.validators import (DataRequired, Email, EqualTo,
                                 Length, ValidationError)

from utlis.forms import _get_fields

from app import bcrypt
from .models import User



class LoginForm(FlaskForm):
    email = StringField('Enter Your Email() : ', validators=(DataRequired(), Email()))
    password = PasswordField('Enter Your Password : ',validators=(DataRequired(),))

    def validate_email(self , email):
        user = User.query.filter(User.email.ilike(f'{email.data}')).first()
        if not user or not bcrypt.check_password_hash(user.password , self.password.data) :
            raise ValidationError('The email or password is incorrect')
    
    def get_fields(self):
        return _get_fields(self)


class RegisterForm(FlaskForm):
    full_name = StringField('Enter Your Full Name : ',
                            validators=(DataRequired()))
    email = StringField('Enter Your Email() : ',
                        validators=(DataRequired(), Email()))
    password = PasswordField('Enter Your Password : ',
                             validators=(DataRequired(), Length(8,128)))
    confirm_password = PasswordField(
        name='Confirm Your Password :',
        validators=(DataRequired(),
                    Length(8,128), EqualTo('confirm_password')))
    
    def validate_email(email):
        _ = User.query.filter(
                User.email.ilike(f'{email.date}'))
        if _:
            raise ValidationError('This Email Already Exists')
    
    def get_fields(self):
        return _get_fields(self)