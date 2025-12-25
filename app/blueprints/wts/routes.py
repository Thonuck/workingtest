from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app.blueprints.wts import bp
from app import db
from app.models import User

def roles_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@bp.route('/create', methods=['GET', 'POST'])
@roles_required(['admin', 'organizer'])  # Sowohl 'admin' als auch 'organizer' dürfen diese Route verwenden
def create():
    return render_template("create.html")
