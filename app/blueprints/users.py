from flask import Blueprint, jsonify, request
from app import db              # ✅ Normaler Import am Anfang!
from app.models import User     # ✅ Normaler Import am Anfang!

bp = Blueprint('users', __name__)

@bp.route('/users')
def list_users():
    # Kein Import hier nötig!
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201


# Proposed from claude:
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User

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