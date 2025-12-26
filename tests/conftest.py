import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key-for-testing-only",
    })

    with app.app_context():
        db.create_all()

        # Test-User anlegen
        user = User(username="testuser")
        user.set_password("secret")
        db.session.add(user)
        db.session.commit()

        yield app

        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()