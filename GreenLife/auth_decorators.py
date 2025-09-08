from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.role.name in roles:
                return f(*args, **kwargs)
            else:
                abort(403)  # Forbidden
        return decorated_function
    return wrapper