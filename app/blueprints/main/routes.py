from flask import render_template, jsonify, request, redirect, url_for
from app.blueprints.main import bp
from app import db
from app.models import Competition

@bp.route('/')
def index():
    # Competition.query.all()
    # print("Hello Visitor!")
    # return render_template('index.html')
    return render_template('index.html')


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
            return render_template("new_working_test.html", title="Neuer Working Test", error="Wettbewerb existiert bereits.")

        new_competition = Competition(name=competition_details["name"],
                                      level=competition_details["class"],
                                      location=competition_details["location"],
                                      date=competition_details["date"])

        db.session.add(new_competition)
        db.session.commit()

        # return render_template("index.html")
        return redirect(url_for('main.index'))
 
    return render_template("new_working_test.html", title="Neuer Working Test")

