import pytest
from flask import url_for

@pytest.fixture
def logged_in_client(client):
    # Log in the user and return the client with the session
    client.post(
        "/users/login",
        data={
            "username": "admin",
            "password": "admin",
        },
        follow_redirects=False
    )

    return client

def test_create_wt(logged_in_client):
    client = logged_in_client

    # Step 2: Create a WT
    response = client.post('/wts/create_wt', data={
        'name': 'Test WT',
        'level': 'Test Level',
        'location': 'Test Location',
        'date': '2024-06-01'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Step 3: Verify the WT appears on the index page
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test WT' in response.data, "Der erstellte WT sollte auf der Index-Seite angezeigt werden."