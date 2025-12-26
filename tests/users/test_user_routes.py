from app.models import User
from app import db


def test_logout(client):
    """Test Logout-Funktionalität"""
    # Zuerst einloggen
    client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "secret",
        }
    )
    
    # Dann ausloggen
    response = client.get(
        "/users/logout",
        follow_redirects=False
    )
    
    assert response.status_code == 302
    assert response.location.endswith('/')


def test_dashboard(client):
    """Test Dashboard-Zugriff als eingeloggter User"""
    # Einloggen
    client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "secret",
        }
    )
    
    # Dashboard aufrufen
    response = client.get("/users/dashboard")
    
    assert response.status_code == 200
    assert b"Willkommen testuser!" in response.data


def test_dashboard_without_login(client):
    """Test Dashboard-Zugriff ohne Login"""
    response = client.get(
        "/users/dashboard",
        follow_redirects=False
    )
    
    # Sollte zu Login umleiten
    assert response.status_code == 302


def test_list_users(client):
    """Test Auflistung aller User"""
    response = client.get("/users/")
    
    assert response.status_code == 200
    # Testuser aus conftest sollte in der Liste sein
    assert b"testuser" in response.data


def test_user_detail(client):
    """Test Detailansicht eines Users"""
    # User-ID aus der Datenbank holen
    with client.application.app_context():
        user = User.query.filter_by(username="testuser").first()
        user_id = user.id
    
    response = client.get(f"/users/{user_id}/detail")
    
    assert response.status_code == 200
    assert b"testuser" in response.data


def test_user_detail_not_found(client):
    """Test Detailansicht mit nicht existierender User-ID"""
    response = client.get("/users/99999/detail")
    
    assert response.status_code == 404


def test_edit_user_get_as_admin(client):
    """Test Edit-Seite GET-Request als Admin"""
    with client.application.app_context():
        admin = User(username="admin_edit", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        
        user_to_edit = User(username="editme")
        user_to_edit.set_password("password")
        db.session.add(user_to_edit)
        db.session.commit()
        
        user_id = user_to_edit.id
    
    # Als Admin einloggen
    client.post(
        "/users/login",
        data={
            "username": "admin_edit",
            "password": "adminpass",
        }
    )
    
    # Edit-Seite aufrufen
    response = client.get(f"/users/{user_id}/edit")
    
    assert response.status_code == 200
    assert b"editme" in response.data


def test_edit_user_post_as_admin(client):
    """Test User bearbeiten als Admin"""
    with client.application.app_context():
        admin = User(username="admin_edit2", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        
        user_to_edit = User(username="editmeplease")
        user_to_edit.set_password("password")
        db.session.add(user_to_edit)
        db.session.commit()
        
        user_id = user_to_edit.id
    
    # Als Admin einloggen
    client.post(
        "/users/login",
        data={
            "username": "admin_edit2",
            "password": "adminpass",
        }
    )
    
    # User bearbeiten
    response = client.post(
        f"/users/{user_id}/edit",
        data={
            "username": "newusername",
            "role": "helper",
        },
        follow_redirects=False
    )
    
    assert response.status_code == 302
    assert "/users/" in response.location
    
    # Prüfen, ob Änderungen gespeichert wurden
    with client.application.app_context():
        edited_user = User.query.get(user_id)
        assert edited_user.username == "newusername"
        assert edited_user.role == "helper"


def test_edit_user_without_permission(client):
    """Test User bearbeiten ohne Admin/Organizer-Rechte"""
    with client.application.app_context():
        user = User.query.filter_by(username="testuser").first()
        user_id = user.id
    
    # Als normaler User einloggen
    client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "secret",
        }
    )
    
    # Versuch User zu bearbeiten
    response = client.get(
        f"/users/{user_id}/edit",
        follow_redirects=False
    )
    
    assert response.status_code == 403


def test_set_user_role_as_admin(client):
    """Test Rolle setzen als Admin"""
    with client.application.app_context():
        admin = User(username="admin_setrole", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        
        user = User(username="changemyrole")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        user_id = user.id
    
    # Als Admin einloggen
    client.post(
        "/users/login",
        data={
            "username": "admin_setrole",
            "password": "adminpass",
        }
    )
    
    # Rolle setzen
    response = client.get(f"/users/set-role/{user_id}/helper")
    
    assert response.status_code == 200
    assert b"helper" in response.data
    
    # Prüfen, ob Rolle gesetzt wurde
    with client.application.app_context():
        changed_user = User.query.get(user_id)
        assert changed_user.role == "helper"


def test_set_user_role_invalid_role(client):
    """Test Rolle setzen mit ungültiger Rolle"""
    with client.application.app_context():
        admin = User(username="admin_setrole2", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        
        user = User(username="invalidrole")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        user_id = user.id
    
    # Als Admin einloggen
    client.post(
        "/users/login",
        data={
            "username": "admin_setrole2",
            "password": "adminpass",
        }
    )
    
    # Ungültige Rolle setzen
    response = client.get(f"/users/set-role/{user_id}/invalidrole")
    
    assert response.status_code == 400
    assert b"Ung" in response.data  # "Ungültige Rolle"


def test_set_user_role_as_organizer(client):
    """Test Rolle setzen als Organizer"""
    with client.application.app_context():
        organizer = User(username="organizer_setrole", role="organizer")
        organizer.set_password("organizerpass")
        db.session.add(organizer)
        
        user = User(username="changemyrole2")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        user_id = user.id
    
    # Als Organizer einloggen
    client.post(
        "/users/login",
        data={
            "username": "organizer_setrole",
            "password": "organizerpass",
        }
    )
    
    # Rolle setzen
    response = client.get(f"/users/set-role/{user_id}/admin")
    
    assert response.status_code == 200
    assert b"admin" in response.data


def test_set_user_role_without_permission(client):
    """Test Rolle setzen ohne Admin/Organizer-Rechte"""
    with client.application.app_context():
        user = User.query.filter_by(username="testuser").first()
        user_id = user.id
    
    # Als normaler User einloggen
    client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "secret",
        }
    )
    
    # Versuch Rolle zu setzen
    response = client.get(f"/users/set-role/{user_id}/admin")
    
    assert response.status_code == 403
