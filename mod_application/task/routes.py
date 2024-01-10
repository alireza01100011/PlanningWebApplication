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


@task.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    form = TaskForm()
    
    user:User = current_user
    user_tasks:Task = user.tasks

    task_manager = TasksManager()
    task_manager.set_tasks(pickle.loads(user_tasks.tasks))
    _task_selected = task_manager.tasks.get(int(id))

    group_manager = GroupManager()
    group_manager.set_groups(pickle.loads(user.groups))

    if not _task_selected:
        return abort(404)

    if request.method == 'GET':
        form.group.choices = [
            (group.id, group.title)
            for group in group_manager.list_groups]
        
        form.title.data = _task_selected.name
        form.start.data = _task_selected.time_start
        form.group.data = _task_selected.group_id


    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('The form is invalid', category='error')
            return render_template('', 
                                    title='Edit Task', form=form)
        
        # Does this group exist? If not, select the default group
        _group = 0 # Defualt ID
        if group_manager.groups.get(form.group.data):
            _group = form.group.data


        task_manager.update_task(
            id = int(id),
            name = form.title.data,
            time_start= form.start.data,
            group_id = _group)
        
        user_tasks.tasks = task_manager.return_tasks_in_pickle

        try:
            db.session.commit()

        except IndentationError:
            db.session.rollback()
            flash('Task editing failed! Please try again', category='error')
        
        else:
            flash('The task was edited successfully', category='success')
            return redirect(url_for('task.manage'))
            
    return render_template('', 
                        title='Edit Task', form=form)

@task.route('remove/<int:id>')
def remove(id:int):
    user:User = current_user
    user_tasks:Task = user.tasks

    task_manager = TasksManager()
    task_manager.set_tasks(pickle.loads(user_tasks.tasks))
    _task_selected = task_manager.tasks.get(int(id))

    if not _task_selected:
        return abort(404)
    
    task_manager.delete_task(int(id))

    user_tasks.tasks = task_manager.return_tasks_in_pickle

    try:
        db.session.commit()
            
    except IndentationError:
        db.session.rollback()
        flash('Something went wrong, please try again', category='error')
    
    else:
        flash('Task delete successfully', category='success')
        redirect(url_for('task.manage'))