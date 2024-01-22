import sys
from flask import render_template, abort, request, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from . import task as buleprint_task
from .models import Task as db_task
from .forms import TaskForm

from ..memory_management.task import TasksManager, _Task
from ..memory_management.group import GroupManager, _Group

sys.path.append("../..")
from mod_user.user.models import User as db_user

from app import db

@buleprint_task.route('/')
def manage():
    # current_user:db_user = current_user

    # task_manager = TasksManager(
    #     pickle_data=current_user.tasks[0].tasks)
    
    
    return render_template('application/to-do.html', title='To Do'
                        ) # tasks=task_manager.list_tasks



@buleprint_task.route('/add', methods=['GET', 'POST'])
def add():
    form = TaskForm()
    current_user:db_user = current_user
    
    group_manager = GroupManager(
        pickle_data=current_user.groups)
    
    
    if request.method == 'GET':
        form.group.choices = [
            (group.id, group.title)
            for group in group_manager.list_groups]
        
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('The form is invalid', category='error')
            return render_template('', 
                                    title='Task', form=form)
        

        task_manager = TasksManager(
            pickle_data=current_user.tasks[0].tasks)
        

        # Does this group exist? If not, select the default group
        _group = 0 # Defualt ID
        if group_manager.groups.get(form.group.data):
            _group = form.group.data
        
        task_manager.add_task(
            name=form.title.data,
            time_start=form.start.data,
            group_id=_group)
        
        current_user.tasks[0].tasks = task_manager.return_tasks_in_pickle

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


@buleprint_task.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    form = TaskForm()
    current_user:db_user = current_user

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
        
        current_user.tasks[0].tasks = task_manager.return_tasks_in_pickle

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


@buleprint_task.route('remove/<int:id>')
def remove(id:int):
    current_user:db_user = current_user

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