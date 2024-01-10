from flask import render_template, request, abort, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from . import event as blueprint_event
from .forms import EventForm
from .models import Event as db_event
from ..memory_management.event import EventManager
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
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Invalid forum', category='error')
            return render_template('',
                                title=' Event ', form=form)
        # --- End IF ----

        event_manager = EventManager(
                pickle_data=current_user.event.events)
        
        # Add New Event
        event_manager.add_event(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start.data,
            end_time=form.end.data,
            reminders=form.reminder.data)
        
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
    return 'edit'

@blueprint_event.route('/delete', methods=['GET'])
def remove():
    return 'remove'



