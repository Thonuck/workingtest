from flask import render_template, jsonify, request, redirect, url_for, flash, session
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
        role = request.form.get('role', 'guest')
        email = request.form.get('email', None)
        user = User(
            username=request.form['username'],
            email=email if email else None,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        flash(f'User {user.username} created successfully.', 'success')
        return redirect(url_for('users.list_users'))
    
    return render_template('users/create.html')

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        email = request.form.get('email', None)
        user.email = email if email else None
        user.role = request.form.get('role', user.role)
        db.session.commit()
        flash(f'User {user.username} updated successfully.', 'success')
        return redirect(url_for('users.user_detail', user_id=user.id))
    
    return render_template('users/edit.html', user=user)

@bp.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Check if trying to delete the current user (when session is available)
    current_user_id = session.get('user_id')
    if current_user_id and current_user_id == user_id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('users.user_detail', user_id=user.id))
    
    # Check if user is an admin
    if user.role == 'admin':
        # Count remaining admin accounts (excluding the one being deleted)
        admin_count = User.query.filter(User.role == 'admin', User.id != user_id).count()
        if admin_count < 1:
            flash('Cannot delete the last admin account. At least one admin must remain.', 'error')
            return redirect(url_for('users.user_detail', user_id=user.id))
    
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been deleted successfully.', 'success')
    return redirect(url_for('users.list_users'))
