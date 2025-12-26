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