def test_login_success(client):
    response = client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "secret",
        },
        follow_redirects=False
    )

    assert response.status_code == 302  # Redirect nach erfolgreichem Login
    assert response.location.endswith('/')


def test_login_failure_wrong_password(client):
    response = client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "wrongpassword",
        },
        follow_redirects=False
    )

    assert response.status_code == 200  # Kein Redirect, Template wird gerendert
    assert b"login" in response.data.lower()  # Login-Seite wird angezeigt


def test_login_failure_wrong_username(client):
    response = client.post(
        "/users/login",
        data={
            "username": "nonexistentuser",
            "password": "secret",
        },
        follow_redirects=False
    )

    assert response.status_code == 200  # Kein Redirect, Template wird gerendert
    assert b"login" in response.data.lower()  # Login-Seite wird angezeigt
