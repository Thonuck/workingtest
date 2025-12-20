from flask import render_template, jsonify, request, redirect, url_for
from app.blueprints.users import bp
from app import db
from app.models import User

@bp.route('/')
def list_users():
    users = User.query.all()
    # Flask sucht automatisch in blueprints/users/templates/users/list.html
    return render_template('users/list.html', users=users)

@bp.route('/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)

@bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user = User(username=request.form['username'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.list_users'))
    
    return render_template('users/create.html')

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        db.session.commit()
        return redirect(url_for('users.user_detail', user_id=user.id))
    
    return render_template('users/edit.html', user=user)

@bp.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.list_users'))


# Proposed from claude:
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Benutzername existiert bereits.')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrierung erfolgreich! Bitte logge dich ein.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login erfolgreich!')
            return redirect(url_for('dashboard'))
        flash('Ungültiger Benutzername oder Passwort.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du wurdest ausgeloggt.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Willkommen {current_user.username}!'