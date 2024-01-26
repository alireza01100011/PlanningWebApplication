import sys
from flask import render_template, request, abort, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from . import event as blueprint_event
from .forms import validate_event_form, EventForm
from .models import Event as db_event
from ..memory_management.event import EventManager, _Event
from ..memory_management.group import GroupManager

from utlis.flask_login import login_required

sys.path.append("../..")
from mod_user.user.models import User as db_user

from app import db


@blueprint_event.route('/', methods=['GET', 'POST'])
@login_required(_next_endpoint='event.manage')
def manage():
    
    user:db_user = db_user.query.get(current_user.id)
    group_manager = GroupManager(
        pickle_data=user.groups)

    
    # Fill in the group field
    groups = [
        (group.id, group.title)
        for group in group_manager.list_groups]

    # manager_event = EventManager(
    #     pickle_data=current_user.event.events)

    if request.method == 'GET':
        return render_template('application/calendar.html',
        title='Events',
        _groups=groups)



@blueprint_event.route('/add', methods=['GET', 'POST'])

def add():

    if request.method == 'GET':
        return redirect(url_for('event.manage'))

    user:db_user = db_user.query.get(current_user.id)
    group_manager = GroupManager(
        pickle_data=user.groups)

    if request.method == 'POST':
        form_data = request.get_json()

        if not validate_event_form(form_data):
            return abort(400)
        # --- End IF ----
        
        event_manager = EventManager(
                pickle_data=user.events[0].events)
        
        _group_id = 0 # Default Group ID
        
        # try: int(form_data['lable'])
        # except KeyError or ValueError: pass
        # else: _id = int(form_data['lable'])
        
        # if group_manager.groups.get(_id):
        #     _group_id = _id
        
        # Add New Event
        event_manager.add_event(
            color='000',
            title=form_data.get('title'),
            description=form_data.get('description'),
            start_time=form_data.get('start'),
            end_time=form_data.get('end'),
            reminders=form_data.get('reminders') or [],
            group=_group_id)
        
        # Seve Data In Pickle
        user.events[0].events = event_manager.return_events_in_pickle

        try:
            db.session.commit()
            
        except IndentationError:
            db.session.rollback()
            flash('Something went wrong, please try again', category='error')
        
        else:
            flash('Event add successfully', category='success')
            redirect(url_for('event.manage'))
        
        return 'OK'

@blueprint_event.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id:int):
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
        current_user.events[0].events = event_manager.return_events_in_pickle

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


@blueprint_event.route('/delete/<int:id>', methods=['GET'])
def remove(id:int):
    current_user:db_user = current_user
    
    event_manager = EventManager(
        pickle_data=current_user.event.events)
    
    _selected_event:_Event|None = \
        event_manager.events.get(int(id))
    
    # EventNot Found 
    if not _selected_event:
        return abort(404)
    # ----

    event_manager.delete_event(int(id))
    
    # Seve Data In Pickle
    current_user.events[0].events = \
        event_manager.return_events_in_pickle
    
    try:
        db.session.commit()
    
    except IndentationError:
        db.session.rollback()
        flash('Something went wrong, please try again', category='error')
    
    else:
        flash('The event was successfully deleted', category='success')
    
    return redirect(url_for('event.manage'))
    



