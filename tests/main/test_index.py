"""Test index route and empty list handling"""
import pytest
from app.models import Competition
from app import db


def test_index_with_empty_competitions(client):
    """Test that index page works correctly with no competitions"""
    # Ensure database is empty
    Competition.query.delete()
    db.session.commit()
    
    response = client.get('/')
    assert response.status_code == 200
    # The page should render without errors even with empty competitions list
    assert b"Wettbewerbe" in response.data or b"Workingtest" in response.data


def test_index_with_competitions(client, app):
    """Test that index page works correctly with competitions"""
    with app.app_context():
        # Create a test competition
        from datetime import date
        comp = Competition(
            name="Test Competition",
            level="A",
            location="Test Location",
            date=date(2026, 3, 1)
        )
        db.session.add(comp)
        db.session.commit()
    
    response = client.get('/')
    assert response.status_code == 200
    assert b"Test Competition" in response.data
