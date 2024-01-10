from flask import render_template, request, abort, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from . import group as buleprint_group
from .forms import GroupForm
from ..memory_management.group import GroupManager

from app import db


@buleprint_group.route('/', methods=['GET'])
def manage():
    group_manager = GroupManager(
        pickle_data=current_user.groupss)

    return render_template('', title='Groups',
                            groups=group_manager.list_groups)


@buleprint_group.route('/add', methods=['GET', 'POST'])
def add():
    form = GroupForm()
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return render_template('',
                    title='Create New Group',form=form)
        # ----

        group_manager = GroupManager(
            pickle_data=current_user.groupss)
        

        group_manager.add_group(
            title=form.title.data,
            color=form.color.data,
            description=form.description.data)
        
        # Save data in the database with (pickled) format
        current_user.groups = group_manager.return_group_in_pickle

        try:
            db.session.commit()

        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')
        
        else:
            flash('New group successfully created', category='success')
            redirect(url_for('group.manage'))
    # ----

    return render_template('',
            title='Create New Group', form=form)



@buleprint_group.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
    form = GroupForm()
    group_manager = GroupManager(
        pickle_data=current_user.groupss)
    
    _selected_group = group_manager.groups.get(int(id))

    # Group Not Found
    if not  _selected_group :
        return abort(404)
    # ----

    if request.method == 'GET':
        form.title.data = _selected_group.title
        form.description.data = _selected_group.description
        form.color.data = _selected_group.color
    # ----

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return render_template('', title='Edit Group', form=form)
        # ----

        group_manager.update_group(
            id=int(id),
            title=form.title.data,
            color=form.color.data,
            description=form.description.data)

        # Save data in the database with (pickled) format
        current_user.groups = group_manager.return_group_in_pickle
        
        try:
            db.session.commit()
            
        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')
        
        else:
            flash('Group edited successfully', category='success')
            redirect(url_for('group.manage'))
    # ----
    
    return render_template('', title='Edit Group', form=form)


@buleprint_group.route('/remove/<int:id>', methods=['GET'])
def remove(id:int):
    group_manager = GroupManager(
        pickle_data=current_user.groupss)
    
    # Group Not Found
    if not group_manager.groups.get(int(id)):
        return abort(404)
    # ----

    group_manager.delete_group(int(id))

    # Save data in the database with (pickled) format
    current_user.groups = group_manager.return_group_in_pickle

    try:
        db.session.commit()
            
    except IndentationError:
        db.session.rollback()
        flash('Something went wrong, please try again', category='error')
    
    else:
        flash('Group delete successfully', category='success')
    
    redirect(url_for('group.manage'))