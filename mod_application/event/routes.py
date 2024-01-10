from flask import render_template, request, abort, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from . import event as blueprint_event
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
    return 'add'

@blueprint_event.route('/edit', methods=['GET', 'POST'])
def edit():
    return 'edit'

@blueprint_event.route('/delete', methods=['GET'])
def remove():
    return 'remove'



