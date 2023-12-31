from flask import ( flash, url_for, redirect,
                    render_template, abort, request)
from flask_login import login_user, logout_user, login_required, current_user

from sqlalchemy.exc import IntegrityError

from . import user
from .models import User
from .forms import LoginForm, RegisterForm

from app import db, bcrypt

@user.route('/', methods=['GET'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login', next=url_for('user.profile')))
    return f'profile <br> Hi,{current_user.full_name}'

@user.route('login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('user/login.html', title='Login', form=form)

    return render_template('user/login.html', title='Login',
                           form=form)


@user.route('register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('user/login.html', title='Login', form=form)

        NewUser = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(
                password=form.password.data)
            )
        
        try:
            db.session.add(NewUser)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Error! Try again (probably because the email you entered already exists)')
            return render_template('user/register.html', title='Register', form=form)
        else:
            flash('Your account has been created successfully')
            return redirect(url_for('user.login'))

    return render_template('user/register.html', title='Register',
                           form=form)
