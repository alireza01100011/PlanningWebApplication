from flask import render_template, request, abort, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from . import event as blueprint_event
from .forms import EventForm
from .models import Event as db_event
from ..memory_management.event import EventManager, _Event
from ..memory_management.group import GroupManager
from ...mod_user.user.models import User as db_user

from app import db


@blueprint_event.route('/', methods=['GET'])
def manage():
    manager_event = EventManager(
        pickle_data=current_user.event.events)
    
    return render_template('', title='Events',
                        events=manager_event.list_events)


@blueprint_event.route('/add', methods=['GET', 'POST'])
def add():
    current_user:db_user = current_user
    form = EventForm()
    
    group_manager = GroupManager(
        pickle_data=current_user.groups)

    if request.method == 'GET':
        # Fill in the group field
        form.group.choices = [
            (group.id, group.title)
            for group in group_manager.list_groups]
    

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return render_template('',
                                title=' Event ', form=form)
        # --- End IF ----

        event_manager = EventManager(
                pickle_data=current_user.event.events)
        

        _group_id = 0 # Default Group ID
        if group_manager.groups.get(int(id)):
            _group_id = form.group.data
        
        # Add New Event
        event_manager.add_event(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start.data,
            end_time=form.end.data,
            reminders=form.reminder.data,
            group=_group_id)
        
        # Seve Data In Pickle
        current_user.events.events = event_manager.return_events_in_pickle

        try:
            db.session.commit()
            
        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')
        
        else:
            flash('Event add successfully', category='success')
            redirect(url_for('event.manage'))

    return render_template('', 
                    title=' Event ', form=form)



@blueprint_event.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EventForm()
    current_user:db_user = current_user
    
    event_manager = EventManager(
        pickle_data=current_user.event.events)
    
    _selected_event:_Event|None = \
        event_manager.events.get(int(id))
    
    # EventNot Found 
    if not _selected_event:
        return abort(404)
    # ----

    group_manager = GroupManager(
        pickle_data=current_user.groups)


    if request.method == 'GET':
        # Fill in the group field
        form.group.choices = [
            (group.id, group.title)
            for group in group_manager.list_groups]
        
        form.title.data = _selected_event.title
        form.end.data = _selected_event.end_time
        form.group.data = _selected_event.group_id
        form.start.data = _selected_event.start_time
        form.reminder.data = _selected_event.reminders
        form.description.data = _selected_event.description

    # ----

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return render_template('',
                                title=' Event ', form=form)
        # ----
        
        _group_id = 0 # Default Group ID
        if group_manager.groups.get(int(id)):
            _group_id = form.group.data
        # ----
            
        # Update Event
        event_manager.update_event(
            id=int(id),
            title=form.title.data,
            description=form.description.data,
            start_time=form.start.data,
            reminders=form.reminder.data,
            group_id=_group_id)
        
        # Seve Data In Pickle
        current_user.events.events = event_manager.return_events_in_pickle

        try:
            db.session.commit()
            
        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')
        
        else:
            flash('Event edited successfully', category='success')
            redirect(url_for('event.manage'))
    # ----
    
    return render_template('', 
                    title=' Event ', form=form)


@blueprint_event.route('/delete', methods=['GET'])
def remove():
    return 'remove'



