from app.models import User
from app import db


def test_register_new_user(client):
    """Test erfolgreiche Registrierung eines neuen Benutzers"""
    response = client.post(
        "/users/register",
        data={
            "username": "newuser",
            "password": "newpassword123",
        },
        follow_redirects=False
    )

    # Sollte zum Login weiterleiten
    assert response.status_code == 302
    assert "/login" in response.location

    # Prüfe, ob der User in der Datenbank existiert
    with client.application.app_context():
        user = User.query.filter_by(username="newuser").first()
        assert user is not None
        assert user.username == "newuser"
        assert user.check_password("newpassword123")
        assert user.role == "guest"  # Default-Rolle


def test_register_duplicate_username(client):
    """Test Registrierung mit bereits existierendem Benutzernamen"""
    response = client.post(
        "/users/register",
        data={
            "username": "testuser",  # Existiert bereits aus conftest
            "password": "somepassword",
        },
        follow_redirects=False
    )

    # Sollte zur Register-Seite zurück weiterleiten
    assert response.status_code == 302
    assert "/register" in response.location


def test_delete_user_as_admin(client):
    """Test Löschen eines Benutzers als Admin"""
    # Zuerst einen Admin-User erstellen und einloggen
    with client.application.app_context():
        admin = User(username="admin_user1", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        
        # Einen zu löschenden User erstellen
        user_to_delete = User(username="deleteme")
        user_to_delete.set_password("password")
        db.session.add(user_to_delete)
        db.session.commit()
        
        user_id = user_to_delete.id

    # Als Admin einloggen
    client.post(
        "/users/login",
        data={
            "username": "admin_user1",
            "password": "adminpass",
        }
    )

    # User löschen
    response = client.post(
        f"/users/{user_id}/delete",
        follow_redirects=False
    )

    # Sollte zur User-Liste weiterleiten
    assert response.status_code == 302

    # Prüfe, ob der User gelöscht wurde
    with client.application.app_context():
        deleted_user = User.query.filter_by(username="deleteme").first()
        assert deleted_user is None


def test_delete_user_as_organizer(client):
    """Test Löschen eines Benutzers als Organizer"""
    # Einen Organizer-User erstellen und einloggen
    with client.application.app_context():
        organizer = User(username="organizer", role="organizer")
        organizer.set_password("organizerpass")
        db.session.add(organizer)
        
        # Einen zu löschenden User erstellen
        user_to_delete = User(username="deleteme2")
        user_to_delete.set_password("password")
        db.session.add(user_to_delete)
        db.session.commit()
        
        user_id = user_to_delete.id

    # Als Organizer einloggen
    client.post(
        "/users/login",
        data={
            "username": "organizer",
            "password": "organizerpass",
        }
    )

    # User löschen
    response = client.post(
        f"/users/{user_id}/delete",
        follow_redirects=False
    )

    # Sollte zur User-Liste weiterleiten
    assert response.status_code == 302

    # Prüfe, ob der User gelöscht wurde
    with client.application.app_context():
        deleted_user = User.query.filter_by(username="deleteme2").first()
        assert deleted_user is None


def test_delete_user_without_permission(client):
    """Test Löschen eines Benutzers ohne Admin/Organizer-Rechte"""
    with client.application.app_context():
        # Einen zu löschenden User erstellen
        user_to_delete = User(username="cantdeleteme")
        user_to_delete.set_password("password")
        db.session.add(user_to_delete)
        db.session.commit()
        
        user_id = user_to_delete.id

    # Als normaler Testuser (guest) einloggen
    client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "secret",
        }
    )

    # Versuch User zu löschen
    response = client.post(
        f"/users/{user_id}/delete",
        follow_redirects=False
    )

    # Sollte 403 Forbidden zurückgeben
    assert response.status_code == 403

    # Prüfe, ob der User NICHT gelöscht wurde
    with client.application.app_context():
        user = User.query.filter_by(username="cantdeleteme").first()
        assert user is not None


def test_delete_nonexistent_user(client):
    """Test Löschen eines nicht existierenden Benutzers"""
    # Als Admin einloggen
    with client.application.app_context():
        admin = User(username="admin_user3", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        db.session.commit()

    client.post(
        "/users/login",
        data={
            "username": "admin_user3",
            "password": "adminpass",
        }
    )

    # Versuche nicht existierenden User zu löschen
    response = client.post(
        "/users/99999/delete",
        follow_redirects=False
    )

    # Sollte 404 zurückgeben
    assert response.status_code == 404


def test_register_password_too_short(client):
    """Test Registrierung mit zu kurzem Passwort"""
    response = client.post(
        "/users/register",
        data={
            "username": "weakuser",
            "password": "ab1",  # Nur 3 Zeichen
        },
        follow_redirects=False
    )

    # Sollte zur Register-Seite zurück weiterleiten
    assert response.status_code == 302
    assert "/register" in response.location

    # Prüfe, ob der User NICHT in der Datenbank existiert
    with client.application.app_context():
        user = User.query.filter_by(username="weakuser").first()
        assert user is None


def test_register_password_no_letter(client):
    """Test Registrierung mit Passwort ohne Buchstaben"""
    response = client.post(
        "/users/register",
        data={
            "username": "numericuser",
            "password": "12345678",  # Nur Zahlen
        },
        follow_redirects=False
    )

    # Sollte zur Register-Seite zurück weiterleiten
    assert response.status_code == 302
    assert "/register" in response.location

    # Prüfe, ob der User NICHT in der Datenbank existiert
    with client.application.app_context():
        user = User.query.filter_by(username="numericuser").first()
        assert user is None


def test_register_password_no_digit(client):
    """Test Registrierung mit Passwort ohne Ziffern"""
    response = client.post(
        "/users/register",
        data={
            "username": "letteruser",
            "password": "abcdefgh",  # Nur Buchstaben
        },
        follow_redirects=False
    )

    # Sollte zur Register-Seite zurück weiterleiten
    assert response.status_code == 302
    assert "/register" in response.location

    # Prüfe, ob der User NICHT in der Datenbank existiert
    with client.application.app_context():
        user = User.query.filter_by(username="letteruser").first()
        assert user is None


def test_register_valid_password(client):
    """Test Registrierung mit gültigem Passwort"""
    response = client.post(
        "/users/register",
        data={
            "username": "validuser",
            "password": "SecurePass123",  # Gültiges Passwort
        },
        follow_redirects=False
    )

    # Sollte zum Login weiterleiten
    assert response.status_code == 302
    assert "/login" in response.location

    # Prüfe, ob der User in der Datenbank existiert
    with client.application.app_context():
        user = User.query.filter_by(username="validuser").first()
        assert user is not None
        assert user.check_password("SecurePass123")
