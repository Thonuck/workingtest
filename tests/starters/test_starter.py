from datetime import date

from sqlalchemy import select

from app import db
from app.models import Competition, Dog, Person, Starter, User


def test_create_starter_with_all_relations(app):
    """Create a Starter linked to a Person, Dog, and Competition, then query it back."""
    with app.app_context():
        person = Person(given_name="Jane", family_name="Doe")
        dog = Dog(name="Rex", breed="Labrador")
        competition = Competition(name="Spring Cup", level="A", location="Berlin", date=date(2025, 5, 1))
        db.session.add_all([person, dog, competition])
        db.session.flush()  # assign IDs without committing

        starter = Starter(
            person_id=person.id,
            dog_id=dog.id,
            competition_id=competition.id,
            paid=True,
            present=False,
            notes="Beginner participant",
        )
        db.session.add(starter)
        db.session.commit()

        # Query using SQLAlchemy 2.0 select()
        result = db.session.execute(
            select(Starter).where(Starter.competition_id == competition.id)
        ).scalars().all()

        assert len(result) == 1
        fetched = result[0]
        assert fetched.person_id == person.id
        assert fetched.dog_id == dog.id
        assert fetched.paid is True
        assert fetched.present is False
        assert fetched.notes == "Beginner participant"


def test_create_starter_without_optional_fields(app):
    """Create a Starter with all optional FK fields as None (no linked entities)."""
    with app.app_context():
        starter = Starter(paid=False, present=False)
        db.session.add(starter)
        db.session.commit()

        result = db.session.execute(
            select(Starter).where(Starter.id == starter.id)
        ).scalar_one()

        assert result.person_id is None
        assert result.dog_id is None
        assert result.competition_id is None
        assert result.notes is None


def test_query_starters_by_competition(app):
    """Create multiple Starters for one Competition and query them by competition_id."""
    with app.app_context():
        competition = Competition(name="Autumn Open", level="F", location="Munich", date=date(2025, 9, 15))
        db.session.add(competition)
        db.session.flush()

        starters = [
            Starter(competition_id=competition.id, paid=True),
            Starter(competition_id=competition.id, paid=False),
            Starter(competition_id=competition.id, paid=True, present=True),
        ]
        db.session.add_all(starters)
        db.session.commit()

        results = db.session.execute(
            select(Starter).where(Starter.competition_id == competition.id)
        ).scalars().all()

        assert len(results) == 3
        paid_starters = [s for s in results if s.paid]
        assert len(paid_starters) == 2


def test_starters_route_uses_db(client, app):
    """Test that the starters route queries starters from the DB, not a static dict."""
    with app.app_context():
        # Create an admin/coach user
        coach = User(username="coach_test", role="coach")
        coach.set_password("coachpass")
        db.session.add(coach)

        person = Person(given_name="Anna", family_name="Müller")
        dog = Dog(name="Bello", breed="Husky")
        competition = Competition(name="Test WT", level="A", location="Berlin", date=date(2025, 6, 1))
        db.session.add_all([person, dog, competition])
        db.session.flush()

        starter = Starter(person_id=person.id, dog_id=dog.id, competition_id=competition.id, starter_number='A1')
        db.session.add(starter)
        db.session.commit()

        competition_id = competition.id

    client.post("/users/login", data={"username": "coach_test", "password": "coachpass"})
    response = client.get(f"/exercises/starters/{competition_id}")

    assert response.status_code == 200
    assert b"Anna" in response.data
    assert b"Bello" in response.data
    assert b"A1" in response.data
