from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.blueprints.starters import bp
from app import db
from app.models import (
    User, Competition, Exercise, ExercisePointEntry, 
    ExerciseResult, Starter, CompetitionResult
)
from app.decorators import roles_required
from sqlalchemy.orm import joinedload


# ==================== WT STARTER PAGE ====================
@bp.route('/starters/<int:competition_id>', methods=['GET', 'POST'])
@login_required
@roles_required(['admin', 'coach'])
def starters(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    starters_db = Starter.query.filter_by(competition_id=competition_id).options(
        joinedload(Starter.person), joinedload(Starter.dog)
    ).all()
    starters = [
        {
            'id': starter.id,
            'number': starter.starter_number or 'unbekannt',
            'name': f"{starter.person.given_name} {starter.person.family_name}" if starter.person else 'unbekannt',
            'dog': starter.dog.name if starter.dog else 'unbekannt',
        }
        for starter in starters_db
    ]

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


