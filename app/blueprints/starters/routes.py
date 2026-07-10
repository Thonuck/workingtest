from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from app import db
from app.blueprints.starters import bp
from app.decorators import roles_required
from app.models import (
    Competition,
    CompetitionResult,
    Dog,
    Exercise,
    ExercisePointEntry,
    ExerciseResult,
    Person,
    Starter,
    User,
)


# ==================== WT STARTER PAGE ====================
@bp.route("/starters/<int:competition_id>", methods=["GET", "POST"])
@login_required
@roles_required(["admin", "coach"])
def starters(competition_id):
    # competition = Competition.query.get_or_404(competition_id)
    starters_db = (
        Starter.query.filter_by(competition_id=competition_id)
        .options(joinedload(Starter.person), joinedload(Starter.dog))
        .all()
    )
    starters = [
        {
            "id": starter.id,
            "number": starter.starter_number or "unbekannt",
            "name": f"{starter.person.given_name} {starter.person.family_name}"
            if starter.person
            else "unbekannt",
            "dog": starter.dog.name if starter.dog else "unbekannt",
        }
        for starter in starters_db
    ]

    table_data = {
        "title": "Starterliste",
        "headers": [
            ("number", "Startnummer"),
            ("name", "Starter Name"),
            ("dog", "Hund"),
        ],
        "items": starters,
        "competition_id": competition_id,
        "details_route": "wts.wt_details",
    }

    return render_template("starters.html.jinja", table_data=table_data)


@bp.route("/starters/<int:competition_id>/<int:starter_id>")
@login_required
@roles_required(["admin", "coach"])
def starter_details(competition_id, starter_id):
    return render_template(
        "starter_details.html.jinja",
        competition_id=competition_id,
        starter_id=starter_id,
    )


@bp.route("starters/<int:competition_id>/add_starter", methods=["GET", "POST"])
@login_required
@roles_required(["admin", "coach"])
def add_starter(competition_id):

    competition = Competition.query.get_or_404(competition_id)
    if request.method == "POST":
        given_name = request.form["given_name"]
        family_name = request.form["family_name"]
        dog_name = request.form["dog_name"]
        dog_breed = request.form["dog_breed"]
        starter_number = request.form["starter_number"]

        if not given_name or not family_name or not dog_name or not dog_breed:
            flash("All required files must befilled.", "danger")
            return redirect(
                url_for("starters.add_starter"), competition_id=competition_id
            )

        person = Person.query.filter_by(
            given_name=given_name, family_name=family_name
        ).first()

        if not person:
            person = Person(given_name=given_name, family_name=family_name)
            db.session.add(person)
            db.session.commit()

        dog = Dog.query.filter_by(name=dog_name, breed=dog_breed).first()
        if not dog:
            dog = Dog(name=dog_name, breed=dog_breed)
            db.session.add(dog)
            db.session.commit()

        existing_starter = Starter.query.filter_by(
            competition_id=competition_id, person_id=person.id, dog_id=dog.id
        ).first()

        if existing_starter:
            flash("Der Starter wurde bereits für den Wettbewerb eingetragen.")
            return render_template(
                url_for("starters.add_starter"), competition_id=competition_id
            )

        new_starter = Starter(
            competition_id=competition.id,
            person_id=person.id,
            dog_id=dog.id,
            starter_number=starter_number if starter_number else None,
        )
        db.session.add(new_starter)
        db.session.commit()

        flash("Starter erfolgreich hinzugefügt!", "success")
        return redirect(url_for("starters.starters", competition_id=competition_id))

    return render_template("new_starter.html.jinja", competition_id=competition_id)
