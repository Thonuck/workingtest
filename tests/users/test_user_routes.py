from app.models import User
from app import db


# ── helper ───────────────────────────────────────────────────────────────────

def _login(client, username, password):
    client.post("/users/login", data={"username": username, "password": password})


def _make_user(client, username, role="guest", password="password"):
    """Create a user in the DB and return their id."""
    with client.application.app_context():
        u = User(username=username, role=role)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return u.id


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
    # Route erfordert Admin/Organizer-Rolle, daher erst als Admin einloggen
    with client.application.app_context():
        admin = User(username="admin_listusers", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)
        db.session.commit()

    client.post(
        "/users/login",
        data={
            "username": "admin_listusers",
            "password": "adminpass",
        }
    )

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


# ── Register page ─────────────────────────────────────────────────────────────

def test_register_page_get(client):
    """GET /register returns 200 with registration form"""
    response = client.get("/users/register")
    assert response.status_code == 200
    assert "Neuen Benutzer registrieren".encode() in response.data
    assert b'name="username"' in response.data
    assert b'name="password"' in response.data


# ── List users ────────────────────────────────────────────────────────────────

def test_list_users_unauthenticated(client):
    """GET /users/ without login redirects to login page"""
    response = client.get("/users/", follow_redirects=False)
    assert response.status_code == 302


def test_list_users_as_guest(client):
    """GET /users/ as guest (no privilege) returns 403"""
    _login(client, "testuser", "secret")
    response = client.get("/users/", follow_redirects=False)
    assert response.status_code == 403


def test_list_users_as_organizer(client):
    """GET /users/ as organizer returns 200"""
    _make_user(client, "org_list", role="organizer", password="orgpass")
    _login(client, "org_list", "orgpass")
    response = client.get("/users/")
    assert response.status_code == 200
    assert b"testuser" in response.data


# ── Edit user ─────────────────────────────────────────────────────────────────

def test_edit_user_get_as_organizer(client):
    """GET /users/<id>/edit as organizer returns 200"""
    uid = _make_user(client, "edit_target_org")
    _make_user(client, "org_edit", role="organizer", password="orgpass")
    _login(client, "org_edit", "orgpass")
    response = client.get(f"/users/{uid}/edit")
    assert response.status_code == 200
    assert b"edit_target_org" in response.data


def test_edit_user_post_as_organizer(client):
    """POST /users/<id>/edit as organizer saves changes and redirects"""
    uid = _make_user(client, "org_edit_target")
    _make_user(client, "org_edit2", role="organizer", password="orgpass")
    _login(client, "org_edit2", "orgpass")
    response = client.post(
        f"/users/{uid}/edit",
        data={"username": "org_renamed", "role": "helper"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    with client.application.app_context():
        u = db.session.get(User, uid)
        assert u.username == "org_renamed"
        assert u.role == "helper"


def test_edit_user_not_found(client):
    """GET/POST /users/99999/edit returns 404"""
    _make_user(client, "admin_editnf", role="admin", password="adminpass")
    _login(client, "admin_editnf", "adminpass")
    assert client.get("/users/99999/edit").status_code == 404
    assert client.post(
        "/users/99999/edit", data={"username": "x", "role": "guest"}
    ).status_code == 404


# ── Set-role ──────────────────────────────────────────────────────────────────

def test_set_user_role_not_found(client):
    """GET /users/set-role/99999/<role> returns 404"""
    _make_user(client, "admin_setrole_nf", role="admin", password="adminpass")
    _login(client, "admin_setrole_nf", "adminpass")
    response = client.get("/users/set-role/99999/helper")
    assert response.status_code == 404


# ── Template content (generic_details-based pages) ────────────────────────────

def test_detail_page_template_content(client):
    """Detail page renders ID, username, role and action buttons via generic_details"""
    with client.application.app_context():
        user = User.query.filter_by(username="testuser").first()
        uid = user.id
    response = client.get(f"/users/{uid}/detail")
    assert response.status_code == 200
    assert b"testuser" in response.data
    assert b"ID" in response.data
    assert "Benutzername".encode() in response.data
    assert "Rolle".encode() in response.data
    assert b"Edit" in response.data
    assert b"Delete" in response.data
    assert b"Back" in response.data


def test_edit_page_template_content(client):
    """Edit page renders form fields for username, role, and password via generic_details"""
    uid = _make_user(client, "tmpl_edit_tgt")
    _make_user(client, "tmpl_admin", role="admin", password="adminpass")
    _login(client, "tmpl_admin", "adminpass")
    response = client.get(f"/users/{uid}/edit")
    assert response.status_code == 200
    assert "Benutzer bearbeiten".encode() in response.data
    assert b'name="username"' in response.data
    assert b'name="role"' in response.data
    assert b'name="password"' in response.data
    assert "Speichern".encode() in response.data
    assert "Abbrechen".encode() in response.data


def test_register_page_template_content(client):
    """Register page renders username and password fields via generic_details"""
    response = client.get("/users/register")
    assert response.status_code == 200
    assert "Neuen Benutzer registrieren".encode() in response.data
    assert b'name="username"' in response.data
    assert b'name="password"' in response.data
    assert "Registrieren".encode() in response.data
