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
    # competition = Competition.query.get_or_404(competition_id)
    # exercises = Exercise.query.filter_by(competition_id=competition_id).all()
    # starters = Starter.query.filter_by(competition_id=competition_id).all()
    starters = [{
        'id': 1,
        'number': "A1",
        'name': 'Starter 1',
        'dog': 'Dog Name 1'
    }, {
        'id': 2,
        'number': "A2",
        'name': 'Starter 2',
        'dog': 'Dog Name 2'
    }]
    
    table_data = {
        'title': "Starterliste",
        'headers': [('number', 'Startnummer'), ('name', 'Starter Name'), ('dog', 'Hund')],
        'items': starters,
        'competition_id': competition_id,
        'details_route': 'wts.wt_details'}
    
    return render_template('index.html.jinja', table_data=table_data)


@bp.route('/starters/<int:competition_id>/<int:starter_id>')
@login_required
@roles_required(['admin', 'coach'])
def starter_details(competition_id, starter_id):
    return render_tamplate('starter_details.html.jinja', competition_id=competition_id, starter_id=starter_id)


