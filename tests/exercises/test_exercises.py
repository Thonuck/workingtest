import pytest
from app import db
from app.models import User, Competition, Exercise, Starter, ExercisePointEntry, CompetitionResult
from datetime import date


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_competition(db_session, name="Test WT"):
    comp = Competition(name=name, level="A", location="Test Location", date=date(2024, 6, 1))
    db_session.add(comp)
    db_session.commit()
    return comp


def _make_exercise(db_session, competition_id, name="Sit", judge_id=None, helper_id=None, max_points=100):
    ex = Exercise(
        name=name,
        competition_id=competition_id,
        judge_id=judge_id,
        helper_id=helper_id,
        max_points=max_points,
    )
    db_session.add(ex)
    db_session.commit()
    return ex


def _login(client, username, password):
    client.post("/users/login", data={"username": username, "password": password})


# ---------------------------------------------------------------------------
# wt_exercises – GET /exercises/wt/<competition_id>
# ---------------------------------------------------------------------------

def test_wt_exercises_as_admin(client):
    """Admin sees all exercises for a competition."""
    with client.application.app_context():
        admin = User(username="admin_ex1", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Admin Exercises WT")
        _make_exercise(db.session, comp.id, "Sit")
        _make_exercise(db.session, comp.id, "Down")
        comp_id = comp.id

    _login(client, "admin_ex1", "adminpass")
    response = client.get(f"/exercises/wt/{comp_id}")

    assert response.status_code == 200
    assert b"Sit" in response.data
    assert b"Down" in response.data


def test_wt_exercises_as_helper_only_assigned(client):
    """Helper only sees exercises they are assigned to."""
    with client.application.app_context():
        helper = User(username="helper_ex1", role="helper")
        helper.set_password("helperpass")
        db.session.add(helper)
        db.session.flush()

        comp = _make_competition(db.session, "Helper Exercises WT")
        _make_exercise(db.session, comp.id, "AssignedExercise", helper_id=helper.id)
        _make_exercise(db.session, comp.id, "UnassignedExercise")
        comp_id = comp.id

    _login(client, "helper_ex1", "helperpass")
    response = client.get(f"/exercises/wt/{comp_id}")

    assert response.status_code == 200
    assert b"AssignedExercise" in response.data
    assert b"UnassignedExercise" not in response.data


def test_wt_exercises_as_guest_returns_403(client):
    """Guest (visitor) cannot access wt_exercises page."""
    with client.application.app_context():
        comp = _make_competition(db.session, "Guest Exercises WT")
        comp_id = comp.id

    _login(client, "testuser", "secret")  # testuser has 'guest' role from conftest
    response = client.get(f"/exercises/wt/{comp_id}")

    assert response.status_code == 403


def test_wt_exercises_unauthenticated_redirects(client):
    """Unauthenticated access redirects to login."""
    with client.application.app_context():
        comp = _make_competition(db.session, "Unauth Exercises WT")
        comp_id = comp.id

    response = client.get(f"/exercises/wt/{comp_id}", follow_redirects=False)
    assert response.status_code == 302


def test_wt_exercises_not_found(client):
    """Returns 404 for non-existing competition."""
    with client.application.app_context():
        admin = User(username="admin_ex404", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        db.session.commit()

    _login(client, "admin_ex404", "adminpass")
    response = client.get("/exercises/wt/99999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# add_exercise – GET/POST /exercises/add/<competition_id>
# ---------------------------------------------------------------------------

def test_add_exercise_get_as_admin(client):
    """Admin can view the add exercise form."""
    with client.application.app_context():
        admin = User(username="admin_add1", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Add Exercise WT")
        comp_id = comp.id

    _login(client, "admin_add1", "adminpass")
    response = client.get(f"/exercises/add/{comp_id}")
    assert response.status_code == 200


def test_add_exercise_post_as_admin(client):
    """Admin can add a new exercise."""
    with client.application.app_context():
        admin = User(username="admin_add2", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Add Exercise POST WT")
        comp_id = comp.id

    _login(client, "admin_add2", "adminpass")
    response = client.post(
        f"/exercises/add/{comp_id}",
        data={"name": "NewExercise", "max_points": "80"},
        follow_redirects=False,
    )

    assert response.status_code == 302

    with client.application.app_context():
        ex = Exercise.query.filter_by(name="NewExercise").first()
        assert ex is not None
        assert ex.max_points == 80
        assert ex.competition_id == comp_id


def test_add_exercise_empty_name_stays_on_form(client):
    """Submitting empty name stays on the add form."""
    with client.application.app_context():
        admin = User(username="admin_add3", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Add Exercise Empty WT")
        comp_id = comp.id

    _login(client, "admin_add3", "adminpass")
    response = client.post(
        f"/exercises/add/{comp_id}",
        data={"name": "", "max_points": "100"},
        follow_redirects=False,
    )

    assert response.status_code == 200  # stays on form


def test_add_exercise_as_guest_returns_403(client):
    """Guest cannot add exercises."""
    with client.application.app_context():
        comp = _make_competition(db.session, "Add Exercise Guest WT")
        comp_id = comp.id

    _login(client, "testuser", "secret")
    response = client.post(
        f"/exercises/add/{comp_id}",
        data={"name": "Should Fail", "max_points": "50"},
        follow_redirects=False,
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# edit_exercise – GET/POST /exercises/edit/<exercise_id>
# ---------------------------------------------------------------------------

def test_edit_exercise_get_as_admin(client):
    """Admin can view the edit exercise form."""
    with client.application.app_context():
        admin = User(username="admin_edit_ex1", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Edit Exercise WT")
        ex = _make_exercise(db.session, comp.id, "EditMe")
        ex_id = ex.id

    _login(client, "admin_edit_ex1", "adminpass")
    response = client.get(f"/exercises/edit/{ex_id}")
    assert response.status_code == 200
    assert b"EditMe" in response.data


def test_edit_exercise_post_as_admin(client):
    """Admin can update an exercise."""
    with client.application.app_context():
        admin = User(username="admin_edit_ex2", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Edit Exercise POST WT")
        ex = _make_exercise(db.session, comp.id, "OldName", max_points=50)
        ex_id = ex.id

    _login(client, "admin_edit_ex2", "adminpass")
    response = client.post(
        f"/exercises/edit/{ex_id}",
        data={"name": "UpdatedName", "max_points": "75"},
        follow_redirects=False,
    )

    assert response.status_code == 302

    with client.application.app_context():
        updated = db.session.get(Exercise, ex_id)
        assert updated.name == "UpdatedName"
        assert updated.max_points == 75


def test_edit_exercise_as_guest_returns_403(client):
    """Guest cannot edit exercises."""
    with client.application.app_context():
        comp = _make_competition(db.session, "Edit Exercise Guest WT")
        ex = _make_exercise(db.session, comp.id, "GuestEdit")
        ex_id = ex.id

    _login(client, "testuser", "secret")
    response = client.get(f"/exercises/edit/{ex_id}", follow_redirects=False)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# delete_exercise – POST /exercises/delete/<exercise_id>
# ---------------------------------------------------------------------------

def test_delete_exercise_as_admin(client):
    """Admin can delete an exercise."""
    with client.application.app_context():
        admin = User(username="admin_del_ex1", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Delete Exercise WT")
        ex = _make_exercise(db.session, comp.id, "DeleteMe")
        ex_id = ex.id
        comp_id = comp.id

    _login(client, "admin_del_ex1", "adminpass")
    response = client.post(f"/exercises/delete/{ex_id}", follow_redirects=False)

    assert response.status_code == 302

    with client.application.app_context():
        assert db.session.get(Exercise, ex_id) is None


def test_delete_exercise_as_guest_returns_403(client):
    """Guest cannot delete exercises."""
    with client.application.app_context():
        comp = _make_competition(db.session, "Delete Exercise Guest WT")
        ex = _make_exercise(db.session, comp.id, "CantDeleteMe")
        ex_id = ex.id

    _login(client, "testuser", "secret")
    response = client.post(f"/exercises/delete/{ex_id}", follow_redirects=False)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# exercise_point_entry – GET /exercises/point-entry/<exercise_id>
# ---------------------------------------------------------------------------

def test_point_entry_as_assigned_helper(client):
    """Assigned helper can access point entry page."""
    with client.application.app_context():
        helper = User(username="helper_pe1", role="helper")
        helper.set_password("helperpass")
        db.session.add(helper)
        db.session.flush()

        comp = _make_competition(db.session, "Point Entry WT")
        ex = _make_exercise(db.session, comp.id, "HelperExercise", helper_id=helper.id)
        ex_id = ex.id

    _login(client, "helper_pe1", "helperpass")
    response = client.get(f"/exercises/point-entry/{ex_id}")
    assert response.status_code == 200


def test_point_entry_unassigned_helper_returns_403(client):
    """Unassigned helper cannot access point entry page."""
    with client.application.app_context():
        helper = User(username="helper_pe2", role="helper")
        helper.set_password("helperpass")
        db.session.add(helper)

        comp = _make_competition(db.session, "Point Entry Unassigned WT")
        ex = _make_exercise(db.session, comp.id, "NotMyExercise")
        ex_id = ex.id

    _login(client, "helper_pe2", "helperpass")
    response = client.get(f"/exercises/point-entry/{ex_id}")
    assert response.status_code == 403


def test_point_entry_as_admin(client):
    """Admin can access any point entry page."""
    with client.application.app_context():
        admin = User(username="admin_pe1", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Point Entry Admin WT")
        ex = _make_exercise(db.session, comp.id, "AdminExercise")
        ex_id = ex.id

    _login(client, "admin_pe1", "adminpass")
    response = client.get(f"/exercises/point-entry/{ex_id}")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# competition_results – GET /exercises/results/<competition_id>
# ---------------------------------------------------------------------------

def test_competition_results_admin_always_visible(client):
    """Admin always sees the full results page."""
    with client.application.app_context():
        admin = User(username="admin_res1", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Results Admin WT")
        comp_id = comp.id

    _login(client, "admin_res1", "adminpass")
    response = client.get(f"/exercises/results/{comp_id}")
    assert response.status_code == 200


def test_competition_results_visitor_unpublished_no_data(client):
    """Visitor sees empty results when not published."""
    with client.application.app_context():
        comp = _make_competition(db.session, "Results Visitor WT")
        comp_id = comp.id

    # No login – anonymous visitor
    response = client.get(f"/exercises/results/{comp_id}")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# publish_results – POST /exercises/publish/<competition_id>
# ---------------------------------------------------------------------------

def test_publish_results_as_admin(client):
    """Admin can publish results."""
    with client.application.app_context():
        admin = User(username="admin_pub1", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Publish Results WT")
        comp_id = comp.id

    _login(client, "admin_pub1", "adminpass")
    response = client.post(f"/exercises/publish/{comp_id}", follow_redirects=False)

    assert response.status_code == 302

    with client.application.app_context():
        result_status = CompetitionResult.query.filter_by(competition_id=comp_id).first()
        assert result_status is not None
        assert result_status.published is True


def test_publish_results_as_guest_returns_403(client):
    """Guest cannot publish results."""
    with client.application.app_context():
        comp = _make_competition(db.session, "Publish Guest WT")
        comp_id = comp.id

    _login(client, "testuser", "secret")
    response = client.post(f"/exercises/publish/{comp_id}", follow_redirects=False)
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# unpublish_results – POST /exercises/unpublish/<competition_id>
# ---------------------------------------------------------------------------

def test_unpublish_results_as_admin(client):
    """Admin can unpublish previously published results."""
    with client.application.app_context():
        admin = User(username="admin_unpub1", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        comp = _make_competition(db.session, "Unpublish Results WT")
        result_status = CompetitionResult(competition_id=comp.id, published=True)
        db.session.add(result_status)
        db.session.commit()
        comp_id = comp.id

    _login(client, "admin_unpub1", "adminpass")
    response = client.post(f"/exercises/unpublish/{comp_id}", follow_redirects=False)

    assert response.status_code == 302

    with client.application.app_context():
        result_status = CompetitionResult.query.filter_by(competition_id=comp_id).first()
        assert result_status.published is False
