import sys
from datetime import datetime

from flask import render_template, abort, request, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from . import task as buleprint_task
from .models import Task as db_task
from .forms import TaskForm

from ..memory_management.task import TasksManager, _Task
from ..memory_management.group import GroupManager, _Group

from utlis.flask_login import login_required
from utlis.time_convert import string_to_int as Time_SI

sys.path.append("../..")
from mod_user.user.models import User as db_user

from app import db

@buleprint_task.route('/')
@login_required(_next_endpoint='task.manage')
def manage():
    user:db_user = db_user.query.get(current_user.id)

    task_manager = TasksManager(
        pickle_data=user.tasks[0].tasks)

    group_manager = GroupManager(
        pickle_data=user.groups)
    
    form = TaskForm()
    form.group.choices = [
        (group.title, group.title)
        for group in group_manager.list_groups]

    return render_template('application/to-do.html', title='To Do',
                       form=form ) # tasks=task_manager.list_tasks



@buleprint_task.route('/add', methods=['POST'])
def add():
    form = TaskForm()
    user:db_user = db_user.query.get(current_user.id)
    
    group_manager = GroupManager(
        pickle_data=user.groups)
    
    form.group.choices = [
        (group.title, group.title)
        for group in group_manager.list_groups]
    if request.method == 'GET':
        return redirect(url_for('task.manage'))
        
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('The form is invalid', category='error')
            return f'Eror'
            return render_template('application/to-do.html', 
                                    title='To Do', form=form)
        
        
        task_manager = TasksManager(
            pickle_data=user.tasks[0].tasks)
        

        # Does this group exist? If not, select the default group
        if group_manager.groups.get(form.group.data):
            _group = form.group.data

        print(Time_SI("2024-10-12 15:00"))

        task_manager.add_task(
            name=form.title.data,
            time_start=Time_SI(str(form.deadline.data), format='%Y-%m-%d'),
            group_title=_group)
        
        user.tasks[0].tasks = task_manager.return_tasks_in_pickle

        try:
            db.session.commit()

        except IndentationError:
            db.session.rollback()
            flash('Task add failed! Please try again', category='error')

        else:
            flash('task added successfully', category='success')
            return redirect(url_for('task.manage'))
     



@buleprint_task.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    form = TaskForm()
    user:db_user = db_user.query.get(current_user.id)

    task_manager = TasksManager(
        pickle_data=current_user.tasks[0].tasks)
    
    _selected_task = task_manager.tasks.get(int(id))

    # Task Not Found
    if not _task_selected:
        return abort(404)
    # ----

    group_manager = GroupManager(
        pickle_data=current_user.groups)
    
    if request.method == 'GET':
        return redirect(url_for('task.manage'))


    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('The form is invalid', category='error')
            return render_template('application/to-do.html', 
                                    title='To Do', form=form)
        
        # Does this group exist? If not, select the default group
        _group = 0 # Defualt ID
        if group_manager.groups.get(form.group.data):
            _group = form.group.data


        task_manager.update_task(
            id = int(id),
            name = form.title.data,
            time_start= form.start.data,
            group_id = _group)
        
        current_user.tasks[0].tasks = task_manager.return_tasks_in_pickle

        try:
            db.session.commit()

        except IndentationError:
            db.session.rollback()
            flash('Task editing failed! Please try again', category='error')
        
        else:
            flash('The task was edited successfully', category='success')
            return redirect(url_for('task.manage'))
            
    return render_template('application/to-do.html', 
                        title='To Do', form=form)


@buleprint_task.route('remove/<int:id>')
def remove(id:int):
    user:db_user = db_user.query.get(current_user.id)

    task_manager = TasksManager(
        pickle_data=current_user.tasks[0].tasks)
    
    _selected_task = task_manager.tasks.get(int(id))

    # Task Not Found
    if not _task_selected:
        return abort(404)
    # ----

    task_manager.delete_task(int(id))

    current_user.tasks[0].tasks = task_manager.return_tasks_in_pickle

    try:
        db.session.commit()
            
    except IndentationError:
        db.session.rollback()
        flash('Something went wrong, please try again', category='error')
    
    else:
        flash('Task delete successfully', category='success')
        redirect(url_for('task.manage'))