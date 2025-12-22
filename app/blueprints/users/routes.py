from flask import render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app.blueprints.users import bp
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

@bp.route('/set-role/<int:user_id>/<role>')
@roles_required(['admin', 'organizer'])  # Sowohl 'admin' als auch 'organizer' dürfen diese Route verwenden
def set_user_role(user_id, role):
    user = User.query.get_or_404(user_id, description="Benutzer nicht gefunden")
    
    # Rolle setzen
    if role not in ['guest', 'helper', 'organizer', 'admin']:
        return "Ungültige Rolle", 400  # Eingabeprüfung für die Rolle

    user.role = role
    db.session.commit()
    return f"Die Rolle von {user.username} wurde auf {role} gesetzt."

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Benutzername existiert bereits.')
            return redirect(url_for('users.register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrierung erfolgreich! Bitte logge dich ein.')
        return redirect(url_for('users.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login erfolgreich!')
            return redirect(url_for('main.index'))
        flash('Ungültiger Benutzername oder Passwort.')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    return f'Willkommen {current_user.username}!'

@bp.route('/')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@roles_required(['admin', 'organizer'])  # Sowohl 'admin' als auch 'organizer' dürfen diese Route verwenden
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.role = request.form['role']
        db.session.commit()
        return redirect(url_for('users.list_users'))
    
    return render_template('edit.html', user=user)

@bp.route('/<int:user_id>/delete', methods=['POST'])
@roles_required(['admin', 'organizer'])  # Sowohl 'admin' als auch 'organizer' dürfen diese Route verwenden
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.list_users'))

def roles_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@bp.route('/set-role/<int:user_id>/<role>')
@roles_required(['admin', 'organizer'])  # Sowohl 'admin' als auch 'organizer' dürfen diese Route verwenden
def set_user_role(user_id, role):
    user = User.query.get(user_id)
    if not user:
        return "Benutzer nicht gefunden", 404
    
    # Rolle setzen
    if role not in ['guest', 'helper', 'organizer', 'admin']:
        return "Ungültige Rolle", 400  # Eingabeprüfung für die Rolle

    user.role = role
    db.session.commit()
    return f"Die Rolle von {user.username} wurde auf {role} gesetzt."

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Benutzername existiert bereits.')
            return redirect(url_for('users.register'))
        new_user = User(username=username)
        # new_user.role = 'guest'
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrierung erfolgreich! Bitte logge dich ein.')
        return redirect(url_for('users.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login erfolgreich!')
            return redirect(url_for('main.index'))
        flash('Ungültiger Benutzername oder Passwort.')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    return f'Willkommen {current_user.username}!'

@bp.route('/')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@roles_required(['admin', 'organizer'])  # Sowohl 'admin' als auch 'organizer' dürfen diese Route verwenden
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        db.session.commit()
        return redirect(url_for('users.user_detail', user_id=user.id))
    
    return render_template('edit.html', user=user)

@bp.route('/<int:user_id>/delete', methods=['POST'])
@roles_required(['admin', 'organizer'])  # Sowohl 'admin' als auch 'organizer' dürfen diese Route verwenden
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.list_users'))
