from flask import render_template, jsonify, request, redirect, url_for
from flask_login import current_user
from app.blueprints.main import bp
from app import db
from app.models import Competition, CompetitionResult
import logging

logger = logging.getLogger()


@bp.route('/')
def index():
    competitions = Competition.query.all()
    
    # Prepare competition data with result status
    comp_data = []
    for comp in competitions:
        result_status = CompetitionResult.query.filter_by(competition_id=comp.id).first()
        is_published = result_status.published if result_status else False
        
        comp_data.append({
            'competition': comp,
            'results_published': is_published
        })
    headers = [("name", "Name"), ("level", "Klasse"), ("location", "Ort"), ("date", "Datum")]

    # Convert Competition objects to dictionaries for template
    items = []
    for comp in competitions:
        items.append({
            'id': comp.id,
            'name': comp.name,
            'level': comp.level,
            'location': comp.location,
            'date': comp.date.strftime('%Y-%m-%d') if comp.date else ''
        })

    table_data = {
        'title': "Wettbewerbe",
        'headers': headers,
        'items': items,
        'details_route': 'wts.wt_details'}

    logger.error("datatable: %s", table_data)
    
    return render_template('index.html.jinja', table_data=table_data)


@bp.route('/about')
def about():
    return render_template("about.html.jinja")


@bp.route('/new_working_test', methods=['GET', 'POST'])
def new_working_test():
    if request.method == 'POST':
        competition_details: dict[str, str] = {"name": request.form.get('wt_name'),
                                               "class": request.form.get('wt_class'),
                                               "location": request.form.get("wt_location"),
                                               "date": request.form.get("wt_date")}
        # Create a new Competition instance
        print("Creating new competition with details: %s", competition_details)

        # check if competition already exists
        existing_competition = Competition.query.filter_by(name=competition_details['name'], 
                                                           level=competition_details['class']).first()

        if existing_competition:
            logger.info(f"Competition already exists: {competition_details['name']}")
            return render_template("new_working_test.html.jinja", title="Neuer Working Test", error="Wettbewerb existiert bereits.")

        new_competition = Competition(name=competition_details["name"],
                                      level=competition_details["class"],
                                      location=competition_details["location"],
                                      date=competition_details["date"])

        db.session.add(new_competition)
        db.session.commit()

        # return render_template("index.html")
        return redirect(url_for('main.index'))
 
    return render_template("new_working_test.html.jinja", title="Neuer Working Test")
