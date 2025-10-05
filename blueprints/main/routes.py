from flask import Blueprint
from flask import render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Starter
from models import db, User, Dog, Competition, Starter, Person
from typing import Optional
import logging

logger = logging.getLogger(__name__)


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def main_index() -> str:
    # get all competitions
    competitions = Competition.query.all()
    print(competitions)


    return render_template("index.html", title="Workingtest Planer", competitions=competitions)


def add_starter_from_names(competition_name: str,
                           given_name: str,
                           family_name: str,
                           dog_name: str,
                           dog_breed: str,
                           notes: str,
                           payment_status=False,
                           attendance_status=False):

    # check if starter already exists
    existing_starter: Optional[Starter] = Starter.query.join(Person).join(Dog).join(Competition).filter(
        Person.given_name == given_name,
        Person.family_name == family_name,
        Dog.name == dog_name,
        Competition.name == competition_name
    ).first()

    if existing_starter:
        logger.info(f"Starter already exists: {given_name} {family_name} with dog {dog_name} in competition {competition_name}")
        return existing_starter

    # Find or create User
    person = Person.query.filter_by(given_name=given_name, family_name=family_name).first()
    if not person:
        person: Person = Person(given_name=given_name, family_name=family_name, email="not@given.com")
        db.session.add(person)
        db.session.flush()  # Assigns user.id before commit

    # Find or create Dog
    dog = Dog.query.filter_by(name=dog_name).first()
    if not dog:
        dog = Dog(name=dog_name, breed=dog_breed)  # Get breed from form if available
        db.session.add(dog)
        db.session.flush()

    # Find or create Competition
    competition = Competition.query.filter_by(name=competition_name).first()
    assert competition != None, "Competition must exist to create a starter"

    # Create Starter
    starter = Starter(
        person_id=person.id,
        dog_id=dog.id,
        competition_id=competition.id,
        paid=payment_status,
        present=attendance_status,
        notes=notes
    )
    db.session.add(starter)
    db.session.commit()
    return starter

@main_bp.route('/starter_details', methods=['GET', 'POST'])
def starter_details():
    if request.method == 'POST':
        # Handle form submission or other POST logic here
        starter_details: dict[str, str] = {"given_name": request.form.get('given_name'),
                                           "family_name": request.form.get('family_name'),
                                           "dog_name": request.form.get("dog_name"),
                                           "dog_breed": request.form.get("dog_breed"),
                                           "notes": request.form.get("notes"),
                                           "payment_status": request.form.get("payment_status"),
                                           "attendance_status": request.form.get("attendance_status"),
                                           "competition": request.form.get("competition")}

        # Create a new StarterModel instance
        new_starter = Starter(
            given_name=starter_details['given_name'],
            family_name=starter_details['family_name'],
            dog_name=starter_details['dog_name'],
            dog_breed=starter_details['dog_breed'],
            notes=starter_details['notes'],
            payment_status=bool(starter_details['payment_status']),
            attendance_status=bool(starter_details['attendance_status'])
        )
        # Create a new database session
        engine = create_engine('sqlite:///starters.db')  # Adjust the database URL as needed
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        # Add the new starter to the session and commit
        session.add(new_starter)
        session.commit()
        # Get the ID of the newly inserted starter
        starter_id = new_starter.id
        # Close the session
        session.close()

        if not starter_id:
            # Handle the case where the insertion failed
            return render_template("starter.html", title="Starter Details", error="Failed to insert starter details.")
        # Redirect to the starter details page or render a success message
        # For simplicity, we will just render the starter details page
        # You might want to redirect to a specific page or show a success message
        # For now, we will just render the starter details page
        # If you want to redirect, you can use:
        return redirect(url_for('main.starter_details', starter_id=starter_id))

        # return render_template("starter.html", title="Starter Details")

    return render_template("starter_details.html", title="Starter Details")


@main_bp.route('/tasks')
def tasks():
    return render_template("tasks.html", title="Aufgaben")

@main_bp.route('/helpers')
def helpers():
    return render_template("helpers.html", title="Aufgaben")

@main_bp.route('/about')
def about():
    return render_template("index_boot.html", title="Aufgaben")

@main_bp.route('/new_working_test', methods=['GET', 'POST'])
def new_working_test():
    if request.method == 'POST':
        competition_details: dict[str, str] = {"name": request.form.get('wt_name'),
                                               "class": request.form.get('wt_class'),
                                               "location": request.form.get("wt_location"),
                                               "date": request.form.get("wt_date")}
        # Create a new Competition instance
        print("Creating new competition with details: %s", competition_details)

        # check if competition already exists
        existing_competition = Competition.query.filter_by(name=competition_details['name']).first()
        if existing_competition:
            logger.info(f"Competition already exists: {competition_details['name']}")
            return render_template("new_working_test.html", title="Neuer Working Test", error="Wettbewerb existiert bereits.")
        new_competition = Competition(name=competition_details["wt_name"],
                                                   level=competition_details["wt_class"],
                                                   location=competition_details["wt_location"],
                                                   date=competition_details["wt_date"])
        db.session.add(new_competition)
        db.session.commit()

        # return render_template("index.html")
        return redirect(url_for('main.main_index'))
 
    return render_template("new_working_test.html", title="Neuer Working Test")


@main_bp.route('/starter', methods=['GET', 'POST'])
def starter():
    if request.method == 'POST':
        print("post")
        return render_template("starter.html", title="Starter")

    return render_template("starter.html", title="Starter", starters={})
