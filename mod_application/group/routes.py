from pickle import dumps, loads

from flask import render_template, request, abort, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from ..memory_management.group import GroupManager

from . import group
from .forms import GroupForm

from app import db


@group.route('/')
def manage():
    # todo : Manage Groups
    return 'Group List'


@group.route('/add', methods=['GET', 'POST'])
def add():
    form = GroupForm()
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return render_template('', title='Create New Group', form=form)
        
        group_manager = GroupManager()
        group_manager.set_groups(loads(current_user.groups))

        group_manager.add_group(
            title=form.title.data,
            color=form.color.data,
            description=form.description.data)
        
        current_user.group = group_manager.return_group_in_pickle
        del group_manager # Free up the RAM
        try:
            db.session.commit()
        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')
        else:
            flash('New group successfully created', category='success')
            redirect(url_for('group.manage'))

    return render_template('', title='Create New Group', form=form)



@group.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    form = GroupForm()
    group_manager = GroupManager()
    group_manager.set_groups(loads(current_user.groups))
    
    _group = group_manager.groups.get(int(id))
    if not  _group :
        del group_manager, _group # Free up the RAM
        return abort(404)

    if request.method == 'GET':
        form.title.data = _group.title
        form.description.data = _group.description
        form.color.data = _group.color

        del group_manager # Free up the RAM
    del _group # Free up the RAM

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return render_template('', title='Edit Group', form=form)
        
        group_manager.update_group(
            id=int(id),
            title=form.title.data,
            color=form.color.data,
            description=form.description.data)

        current_user.group = group_manager.return_group_in_pickle
        del group_manager # Free up the RAM
        
        try:
            db.session.commit()
            
        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')
        
        else:
            flash('Group edited successfully', category='success')
            redirect(url_for('group.manage'))

    return render_template('', title='Edit Group', form=form)


@group.route('/remove/<int:id>')
def remove(id:int):
    # todo : Remve group
    return 'remove group'