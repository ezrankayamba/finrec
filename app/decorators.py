from functools import wraps
from flask import g, request, redirect, url_for, flash
from flask_login import current_user


def fx_rec_group_resource(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user is None:
            return redirect(url_for('users.login', next=request.url))
        if current_user.role != 'ADMIN' or current_user.group is None:
            flash('You are not authorized to access requested resource')
            return redirect(url_for('users.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
