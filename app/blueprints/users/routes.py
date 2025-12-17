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
