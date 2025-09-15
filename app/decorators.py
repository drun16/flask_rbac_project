# app/decorators.py

from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(role_name):
    """
    A decorator to protect routes that require a specific role.
    If the current user does not have the required role, it aborts with a 403 error.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role_name):
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator