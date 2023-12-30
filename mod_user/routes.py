from flask import (
                    render_template, abort, request)


from . import user
from .models import User
from .forms import LoginForm, RegisterForm

from app import db, bcrypt

@user.route('login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        pass

    return render_template('user/login.html', title='Login',
                           form=form)


@user.route('register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        pass

    return render_template('user/register.html', title='Register',
                           form=form)
