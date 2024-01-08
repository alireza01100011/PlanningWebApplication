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


@group.route('/add')
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



@groups.route('/edit/<int:id>')
def edit(id:int):

    return render_template('', title='Edit Group', form=form)


@group.route('/remove/<int:id>')
def remove(id:int):
    # todo : Remve group
    return 'remove group'