from functools import wraps

from flask import redirect, url_for, flash, abort
from flask_login import current_user


def not_logged_in(_redirect:str):
    def getfunc(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return func(*args, **kwargs)
            flash('You are already logged in .')
            return redirect(url_for(_redirect))
        
        return wrapper
    return getfunc

def login_required(
        _next_endpoint:str=None,
        _next_url:str=None,
        _login_path:str='user.login',
        _f_msg:str = 'You do not have access, login first !',
        _f_cat:str='message'
        ):
    def getfunc(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                return func(*args, **kwargs)
            
            flash(message=_f_msg, category=_f_cat)
            
            if (_login_path) and (not _next_endpoint):
                return redirect(
                    url_for(_login_path, next=_next_url))
            
            if (_login_path) and (not _next_url):
                return redirect(
                    url_for(_login_path, next=url_for(_next_endpoint)))
            
            return abort(401)
        return wrapper
    return getfunc
