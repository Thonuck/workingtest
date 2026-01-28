from functools import wraps
from flask import abort
from flask_login import current_user


def roles_required(roles):
    """
    Decorator to restrict route access to users with specific roles.
    
    Args:
        roles: List of role names that are allowed to access the route
        
    Returns:
        Decorated function that checks user authentication and role
        
    Raises:
        403: If user is not authenticated or doesn't have required role
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
