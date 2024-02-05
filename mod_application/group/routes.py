from flask import render_template, request, abort, flash, redirect, url_for, jsonify
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from . import group as buleprint_group
from .forms import GroupForm
from ..memory_management.group import GroupManager

from utlis.dictionary import COLORs as COLORS
from app import db

COLORs = COLORS()

@buleprint_group.route('/', methods=['GET'])
def manage():
    group_manager = GroupManager(
        pickle_data=current_user.groups)
    form = GroupForm()

    return render_template('application/group.html',
        title='Groups', groups=group_manager.list_groups,
        form=form, colors_dict=COLORs.colors_bootstrap)


@buleprint_group.route('/add', methods=['GET', 'POST'])
def add():
    form = GroupForm()
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return redirect(url_for('group.manage'))
        # ----

        group_manager = GroupManager(
            pickle_data=current_user.groups)
        

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

    return redirect(url_for('group.manage'))



@buleprint_group.route('/edit/<string:title>', methods=['GET', 'POST'])
def edit(title:str):
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


@buleprint_group.route('/remove/<string:title>', methods=['GET'])
def remove(title:str):
    group_manager = GroupManager(
        pickle_data=current_user.groups)
    
    
    # Group Not Found
    if not group_manager.groups.get(str(title)):
        flash('Not Found Group, 404!', category='error')
        return redirect(url_for('group.manage'))
    # ----

    group_manager.delete_group(str(title))

    # Save data in the database with (pickled) format
    current_user.groups = group_manager.return_group_in_pickle

    try:
        db.session.commit()
            
    except IndentationError:
        db.session.rollback()
        flash('Something went wrong, please try again', category='error')
    
    else:
        flash('Group delete successfully', category='success')
    
    return redirect(url_for('group.manage'))


@buleprint_group.route('/json/get', methods=['GET'])
def send_json():
    group_manager = GroupManager(
        pickle_data=current_user.groups)
    
    data = {
        group.title : group.color
        for group in group_manager.groups.values()
        }
    
    return jsonify(data)