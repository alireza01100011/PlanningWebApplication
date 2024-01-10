import pickle

from flask import render_template, abort, request, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from utlis.flask_login import login_required
from ..memory_management.task import TasksManager
from ..memory_management.group import GroupManager
from .models import Task
from .forms import TaskForm
from . import task


from dateabase_models._models import User, Task, Event

from app import db

@task.route('/')
def manage():
    return 'hello world'


@task.route('/add', methods=['GET', 'POST'])
def add():
    form = TaskForm()
    user = current_user
    group_manager = GroupManager()
    group_manager.set_groups(pickle.loads(user.groups))
    
    if request.method == 'GET':
        form.group.choices = [
            (group.id, group.title)
            for group in group_manager.list_groups]
        
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('The form is invalid', category='error')
            return render_template('', 
                                    title='Task', form=form)
        
        user_tasks = user.tasks
        user_tasks:Task = user_tasks[0]

        task_manager = TasksManager()
        task_manager.set_tasks(pickle.loads(user_tasks.tasks))

        # Does this group exist? If not, select the default group
        _group = 0 # Defualt ID
        if group_manager.groups.get(form.group.data):
            _group = form.group.data
        
        task_manager.add_task(
            name=form.title.data,
            time_start=form.start.data,
            group_id=_group)
        
        user_tasks.tasks = task_manager.return_tasks_in_pickle

        try:
            db.session.commit()

        except IndentationError:
            db.session.rollback()
            flash('Task add failed! Please try again', category='error')

        else:
            flash('task added successfully', category='success')
            return redirect(url_for('task.manage'))
     
    return render_template('', 
                        title='Task', form=form)

