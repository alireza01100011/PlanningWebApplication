from flask import ( flash, url_for, redirect,
                    render_template, abort, request)
from flask_login import login_user, logout_user, current_user

from sqlalchemy.exc import IntegrityError

from . import user
from .models import User
from .forms import LoginForm, RegisterForm, SettingForm

from app import db, bcrypt

from utlis.flask_login import not_logged_in, login_required
from mod_application.memory_management.group import GroupManager
from mod_application.memory_management.task import TasksManager
from mod_application.memory_management.event import EventManager

from dateabase_models._models import Event, Task

@user.route('/', methods=['GET'])
@login_required(_next_url='/profile/')
def profile():

    return render_template('user/profile.html',
    title='Profile', 
    task_total='1258', task_done_total='180',
    event_total='180', event_done_total='175')


@user.route('login/', methods=['GET', 'POST'])
@not_logged_in('user.profile')
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('user/forms-A.html', title='Login', form=form)

        user = User.query.filter(User.email.ilike(f'{form.email.data}')).first()
        if not user:
            flash("Something went wrong. Please try again")
            return render_template('user/forms-A.html', title='Login', form=form)
        
        login_user(user, remember=form.remember.data)
        flash('You have successfully logged in' , 'info')
        __next = request.args.get('next', type=str,
                                  default=url_for('user.profile'))
        return redirect(__next)

    return render_template('user/forms-A.html', title='Login',
                           form=form)


@user.route('register/', methods=['GET', 'POST'])
@not_logged_in('user.profile')
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('user/forms-A.html', title='Register', form=form)
        
        # Remaining: Email confirmation must be added
        
        NewUser = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(
                            password=form.password.data)
            )
        
        NewUser.groups = GroupManager().return_group_in_pickle
        
        # Create Roll Task And Event 
        NewTask = Task(
            TasksManager().return_tasks_in_pickle)
        NewEvent = Event(
            TasksManager().return_tasks_in_pickle)

        # Create Relation 
        NewTask.user = NewUser
        NewEvent.user = NewUser

        try:
            db.session.add_all([NewEvent, NewTask, NewUser])
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            flash('Error! Try again (probably because the email you entered already exists)')
            return render_template('user/forms-A.html', title='Register', form=form)

        else:
            flash('Your account has been created successfully')
            return redirect(url_for('user.login'))

    return render_template('user/forms-A.html', title='Register',
                           form=form)


@user.route('logout/', methods=['GET'])
@login_required()
def logout():
    user = current_user
    if not user :
        flash('A rare problem occurred, logout failed! Try again ...')
        return redirect(url_for('user.profile'))
    
    logout_user()
    flash('Logout was successful.')
    return redirect('/')


@user.route('settings/', methods=['GET', 'POST'])
@login_required(_next_endpoint='user.settings')
def settings():
    form  = SettingForm()
    user = current_user
    if request.method == 'GET':
        form.email.data = user.email
        form.full_name.data = user.full_name
        
        form.old_password.data, form.password.data,\
            form.confirm_password.data  = '*'*8, '*'*8, '*'*8
        
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('user/settings.html', title='Setting Account',
                        form=form, submit_button='Update')
        
        user.full_name = form.full_name.data

        # Checks that in the password fields ([not 8 stars] : '*'*8 )
        _password_not_asterisk = '*'*8 in [form.confirm_password.data, 
                                           form.old_password.data, form.password.data]
        
        # Checks that the user has entered the account password correctly
        _password_must_be_correct = bcrypt.check_password_hash(
                                    user.password, form.old_password.data)\
                                    if not _password_not_asterisk else False
        
        if _password_must_be_correct :
            user.password = bcrypt.generate_password_hash(form.password.data)
    
        if not form.email.data == user.email:
            # Remaining: Email confirmation must be added
            user.email = form.email.data

        try:
            db.session.commit()
        except IntegrityError:
            flash('Updating your profile information failed! Please try again.')
            db.session.rollback()
        else:
            flash('Your profile information has been successfully updated .')
            
            if _password_must_be_correct:
                flash('Your password has been successfully updated .')

    return render_template('user/settings.html', title='Setting Account',
                           form=form, submit_button='Update')










