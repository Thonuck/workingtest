
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.blueprints.starters import bp
from app import db
from app.models import (
    User, Competition, Exercise, ExercisePointEntry, 
    ExerciseResult, Starter, CompetitionResult
)
from app.decorators import roles_required


# ==================== WT STARTER PAGE ====================
@bp.route('/starters/<int:competition_id>', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'coach'])
def starters(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    exercises = Exercise.query.filter_by(competition_id=competition_id).all()
    starters = Starter.query.filter_by(competition_id=competition_id).all()

    return render_template(
        'starters/starters.html.jinja',
        competition=competition,
        exercises=exercises,
        starters=starters
    )
