
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from app.blueprints.starters import bp
from app import db
from app.models import (
    User, Competition, Exercise, ExercisePointEntry, 
    ExerciseResult, Starter, CompetitionResult
)


def roles_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ==================== WT STARTER PAGE ====================
@bp.route('/starters/<int:competition_id>', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'coach'])
def starters(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    exercises = Exercise.query.filter_by(competition_id=competition_id).all()
    starters = Starter.query.filter_by(competition_id=competition_id).all()

    if request.method == 'POST':
        starter_name = request.form.get('starter_name')
        if not starter_name:
            flash('Bitte geben Sie einen Namen für den Starter ein.', 'danger')
            return redirect(url_for('starters.starters', competition_id=competition_id))

        new_starter = Starter(name=starter_name, competition_id=competition_id)
        db.session.add(new_starter)
        db.session.commit()
        flash(f'Starter "{starter_name}" wurde hinzugefügt.', 'success')
        return redirect(url_for('starters.starters', competition_id=competition_id))

    return render_template(
        'starters/starters.html',
        competition=competition,
        exercises=exercises,
        starters=starters
    )
