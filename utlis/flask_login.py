from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def not_logged_in(_redirect:str):
    def getfunc(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return func(*args, **kwargs)
            
            return redirect(url_for(_redirect))
        
        return wrapper
    return getfunc