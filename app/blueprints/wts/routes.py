from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app.blueprints.wts import bp
from app import db
from app.models import User, Competition
from datetime import date as dt_date

def roles_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@bp.route('/wts/details/<int:competition_id>')
def wt_details(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    return render_template('wt_details.html', competition=competition)

@bp.route('/create_wt', methods=['GET', 'POST'])
@roles_required(['admin', 'organizer'])  # Sowohl 'admin' als auch 'organizer' dürfen diese Route verwenden
def create_wt():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        level = (request.form.get('level') or '').strip()
        location = (request.form.get('location') or '').strip()
        date_str = (request.form.get('date') or '').strip()

        if not name or not level or not location or not date_str:
            flash('Bitte alle Felder ausfüllen.', 'danger')
            return render_template('create_wt.html')

        try:
            comp_date = dt_date.fromisoformat(date_str)
        except ValueError:
            flash('Ungültiges Datum. Bitte im Format YYYY-MM-DD eingeben.', 'danger')
            return render_template('create_wt.html')

        # Optional: Duplikate vermeiden (Name + Klasse)
        existing = Competition.query.filter_by(name=name, level=level).first()
        if existing:
            flash('Wettbewerb existiert bereits für diese Klasse.', 'warning')
            return render_template('create_wt.html')

        competition = Competition(name=name, level=level, location=location, date=comp_date)
        db.session.add(competition)
        db.session.commit()
        flash('Workingtest erfolgreich erstellt.', 'success')
        return redirect(url_for('main.index'))

    return render_template("create_wt.html")

@bp.route('/delete_wt/<int:competition_id>', methods=['POST'])
@login_required
@roles_required(['admin', 'organizer'])
def delete_wt(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    db.session.delete(competition)
    db.session.commit()
    flash('Working test deleted successfully.', 'success')
    return redirect(url_for('main.index'))
