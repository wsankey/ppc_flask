# project/decorators.py


from functools import wraps
from flask import abort 
from flask import flash, redirect, url_for
from flask.ext.login import current_user
from project.models import *

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def permissions_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not current_user.can(permission):
				abort(403)
			return f(*args, **kwargs)
		return decorated_function
	return decorator

def admin_required(f):
	return permissions_required(Permission.ADMINISTER)(f)

def artist_required(f):
	return permissions_required(Permission.SELL)(f)