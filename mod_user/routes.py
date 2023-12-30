from flask import (
                    render_template, abort, request)


from . import user, User

from app import db, bcrypt

@user.route('login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass

    return render_template('user/login.html', title='Login')


@user.route('register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass

    return render_template('user/register.html', title='Register')
