"""
Unit tests for generic_table.html.jinja template

This module tests the generic table template and its macros including:
- generic_table macro with responsive layouts
- flash_messages macro
- normal_table macro
- clickable_table_row macro
- card_list macro for mobile view
- generic_wide_table macro for desktop view
"""

import pytest
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, flash, url_for


@pytest.fixture
def jinja_env(app):
    """Provide access to the app's Jinja environment with the template loaded."""
    with app.app_context():
        yield app.jinja_env


@pytest.fixture
def sample_table_data():
    """Sample data for testing the generic table."""
    return {
        "title": "Test Table",
        "headers": [
            ("name", "Name"),
            ("email", "Email"),
            ("status", "Status")
        ],
        "items": [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "status": "Active"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "status": "Inactive"},
        ],
        "details_route": "wts.wt_details"
    }


@pytest.fixture
def empty_table_data():
    """Empty table data for testing no items scenario."""
    return {
        "title": "Empty Table",
        "headers": [("name", "Name"), ("email", "Email")],
        "items": [],
        "details_route": "wts.wt_details"
    }


class TestFlashMessagesMacro:
    """Tests for the flash_messages macro."""
    
    def test_flash_messages_displays_single_message(self, app):
        """Test that a single flash message is displayed correctly."""
        template = """
        {% from 'generic_table.html.jinja' import flash_messages %}
        {{ flash_messages() }}
        """
        
        with app.test_request_context():
            flash("Test message", "success")
            rendered = render_template_string(template)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            alert = soup.find('div', class_='alert')
            assert alert is not None
            assert 'alert-success' in alert.get('class')
            assert 'Test message' in alert.text
    
    def test_flash_messages_displays_multiple_messages(self, app):
        """Test that multiple flash messages are displayed."""
        template = """
        {% from 'generic_table.html.jinja' import flash_messages %}
        {{ flash_messages() }}
        """
        
        with app.test_request_context():
            flash("Success message", "success")
            flash("Error message", "danger")
            rendered = render_template_string(template)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            alerts = soup.find_all('div', class_='alert')
            assert len(alerts) == 2
            assert 'Success message' in alerts[0].text
            assert 'Error message' in alerts[1].text
    
    def test_flash_messages_empty_when_no_messages(self, app):
        """Test that no alerts are shown when there are no flash messages."""
        template = """
        {% from 'generic_table.html.jinja' import flash_messages %}
        {{ flash_messages() }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            alerts = soup.find_all('div', class_='alert')
            assert len(alerts) == 0


class TestNormalTableMacro:
    """Tests for the normal_table macro."""
    
    def test_normal_table_creates_table_structure(self, app):
        """Test that normal_table creates proper HTML table structure."""
        template = """
        {% from 'generic_table.html.jinja' import normal_table %}
        {% call normal_table(['Header 1', 'Header 2', 'Header 3']) %}
            <tr><td>Data 1</td><td>Data 2</td><td>Data 3</td></tr>
        {% endcall %}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            # Check table structure
            table = soup.find('table')
            assert table is not None
            assert 'table' in table.get('class')
            assert 'table-striped' in table.get('class')
            assert 'table-hover' in table.get('class')
            
            # Check headers
            headers = table.find('thead').find_all('th')
            assert len(headers) == 3
            assert headers[0].text == 'Header 1'
            assert headers[1].text == 'Header 2'
            assert headers[2].text == 'Header 3'
            
            # Check tbody exists and contains data
            tbody = table.find('tbody')
            assert tbody is not None
            assert 'Data 1' in tbody.text


class TestClickableTableRowMacro:
    """Tests for the clickable_table_row macro."""
    
    def test_clickable_row_has_onclick_handler(self, app):
        """Test that clickable rows have onclick handler and cursor style."""
        template = """
        {% from 'generic_table.html.jinja' import clickable_table_row %}
        {% call clickable_table_row('/test/url') %}
            <td>Cell content</td>
        {% endcall %}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            row = soup.find('tr')
            assert row is not None
            assert row.get('onclick') == "window.location='/test/url'"
            assert 'cursor: pointer' in row.get('style')
            assert 'Cell content' in row.text


class TestCardListMacro:
    """Tests for the card_list macro (mobile view)."""
    
    def test_card_list_displays_items_as_cards(self, app, sample_table_data):
        """Test that card_list renders items as Bootstrap cards."""
        template = """
        {% from 'generic_table.html.jinja' import card_list %}
        {{ card_list(
            table_data.title,
            table_data.headers,
            table_data['items'],
            table_data.details_route
        ) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=sample_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            cards = soup.find_all('div', class_='card')
            assert len(cards) == 2  # Two items in sample data
            
            # Check first card
            first_card = cards[0]
            assert 'cursor: pointer' in first_card.get('style')
            assert first_card.get('onclick') is not None
            
            card_body = first_card.find('div', class_='card-body')
            assert 'John Doe' in card_body.text
            assert 'john@example.com' in card_body.text
    
    def test_card_list_shows_message_for_empty_items(self, app, empty_table_data):
        """Test that card_list shows appropriate message when no items."""
        template = """
        {% from 'generic_table.html.jinja' import card_list %}
        {{ card_list(
            table_data.title,
            table_data.headers,
            table_data['items'],
            table_data.details_route
        ) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=empty_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            alert = soup.find('div', class_='alert-info')
            assert alert is not None
            assert 'Keine Einträge verfügbar' in alert.text
    
    def test_card_list_with_competition_id(self, app, sample_table_data):
        """Test that card_list handles optional competition_id parameter."""
        template = """
        {% from 'generic_table.html.jinja' import card_list %}
        {{ card_list(
            table_data.title,
            table_data.headers,
            table_data['items'],
            table_data.details_route,
            42
        ) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=sample_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            cards = soup.find_all('div', class_='card')
            assert len(cards) == 2


class TestGenericWideTableMacro:
    """Tests for the generic_wide_table macro (desktop view)."""
    
    def test_generic_wide_table_renders_table(self, app, sample_table_data):
        """Test that generic_wide_table renders table with all items."""
        template = """
        {% from 'generic_table.html.jinja' import generic_wide_table %}
        {{ generic_wide_table(
            table_data.title,
            table_data.headers,
            table_data['items'],
            table_data.details_route
        ) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=sample_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            table = soup.find('table')
            assert table is not None
            
            # Check headers
            headers = table.find_all('th')
            assert len(headers) == 3
            assert 'Name' in headers[0].text
            assert 'Email' in headers[1].text
            assert 'Status' in headers[2].text
            
            # Check rows
            rows = table.find('tbody').find_all('tr')
            assert len(rows) == 2
            
            # Check first row data
            first_row_cells = rows[0].find_all('td')
            assert 'John Doe' in first_row_cells[0].text
            assert 'john@example.com' in first_row_cells[1].text
            assert 'Active' in first_row_cells[2].text
    
    def test_generic_wide_table_shows_empty_message(self, app, empty_table_data):
        """Test that generic_wide_table shows message when no items."""
        template = """
        {% from 'generic_table.html.jinja' import generic_wide_table %}
        {{ generic_wide_table(
            table_data.title,
            table_data.headers,
            table_data['items'],
            table_data.details_route
        ) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=empty_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            table = soup.find('table')
            row = table.find('tbody').find('tr')
            cell = row.find('td')
            
            assert cell.get('colspan') == '2'
            assert 'text-center' in cell.get('class')
            assert 'Keine Einträge verfügbar' in cell.text


class TestGenericTableMacro:
    """Tests for the main generic_table macro."""
    
    def test_generic_table_renders_complete_structure(self, app, sample_table_data):
        """Test that generic_table renders with all components."""
        template = """
        {% from 'generic_table.html.jinja' import generic_table %}
        {{ generic_table(table_data) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=sample_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            # Check main structure
            card = soup.find('div', class_='card')
            assert card is not None
            
            # Check title
            title = soup.find('h1', class_='card-title')
            assert title is not None
            assert 'Test Table' in title.text
            
            # Check desktop table container
            desktop_container = soup.find('div', class_='table-container')
            assert desktop_container is not None
            assert 'd-none' in desktop_container.get('class')
            assert 'd-md-block' in desktop_container.get('class')
            
            # Check mobile card container
            mobile_container = soup.find('div', class_='card-container')
            assert mobile_container is not None
            assert 'd-block' in mobile_container.get('class')
            assert 'd-md-none' in mobile_container.get('class')
    
    def test_generic_table_shows_flash_messages_by_default(self, app, sample_table_data):
        """Test that flash messages are shown by default."""
        template = """
        {% from 'generic_table.html.jinja' import generic_table %}
        {{ generic_table(table_data) }}
        """
        
        with app.test_request_context():
            flash("Test notification", "info")
            rendered = render_template_string(template, table_data=sample_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            alert = soup.find('div', class_='alert')
            assert alert is not None
            assert 'Test notification' in alert.text
    
    def test_generic_table_hides_flash_when_disabled(self, app, sample_table_data):
        """Test that flash messages can be hidden with show_flash=false."""
        template = """
        {% from 'generic_table.html.jinja' import generic_table %}
        {{ generic_table(table_data, show_flash=false) }}
        """
        
        with app.test_request_context():
            flash("Test notification", "info")
            rendered = render_template_string(template, table_data=sample_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            alerts = soup.find_all('div', class_='alert')
            # No alerts should be present (or only Bootstrap alerts from the structure)
            assert all('Test notification' not in alert.text for alert in alerts)
    
    def test_generic_table_with_competition_id(self, app, sample_table_data):
        """Test that generic_table handles optional competition_id."""
        sample_table_data['competition_id'] = 42
        template = """
        {% from 'generic_table.html.jinja' import generic_table %}
        {{ generic_table(table_data) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=sample_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            # Just verify it renders without errors
            card = soup.find('div', class_='card')
            assert card is not None
    
    def test_generic_table_handles_empty_data(self, app, empty_table_data):
        """Test that generic_table handles empty items gracefully."""
        template = """
        {% from 'generic_table.html.jinja' import generic_table %}
        {{ generic_table(table_data) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=empty_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            # Check that the title is still displayed
            title = soup.find('h1', class_='card-title')
            assert 'Empty Table' in title.text
            
            # Check that "no items" message appears
            rendered_text = rendered.lower()
            assert 'keine einträge verfügbar' in rendered_text


class TestGenericTableDataStructure:
    """Tests for validating table data structure requirements."""
    
    def test_table_data_with_all_required_fields(self, app):
        """Test that table_data requires all necessary fields."""
        table_data = {
            "title": "Complete Table",
            "headers": [("id", "ID"), ("name", "Name")],
            "items": [{"id": 1, "name": "Test"}],
            "details_route": "wts.wt_details"
        }
        
        template = """
        {% from 'generic_table.html.jinja' import generic_table %}
        {{ generic_table(table_data) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=table_data)
            assert rendered is not None
            assert 'Complete Table' in rendered
    
    def test_headers_are_tuples_of_key_and_display_name(self, app):
        """Test that headers follow (key, display_name) tuple structure."""
        table_data = {
            "title": "Test",
            "headers": [
                ("field1", "Field One"),
                ("field2", "Field Two")
            ],
            "items": [{"id": 1, "field1": "Value1", "field2": "Value2"}],
            "details_route": "wts.wt_details"
        }
        
        template = """
        {% from 'generic_table.html.jinja' import generic_table %}
        {{ generic_table(table_data) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            # Verify display names are used
            assert 'Field One' in rendered
            assert 'Field Two' in rendered


class TestGenericTableResponsiveness:
    """Tests for responsive behavior of generic_table."""
    
    def test_desktop_view_has_correct_classes(self, app, sample_table_data):
        """Test that desktop view uses correct Bootstrap visibility classes."""
        template = """
        {% from 'generic_table.html.jinja' import generic_table %}
        {{ generic_table(table_data) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=sample_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            desktop = soup.find('div', class_='table-container')
            assert 'd-none' in desktop.get('class')  # Hidden on small screens
            assert 'd-md-block' in desktop.get('class')  # Visible on medium+
    
    def test_mobile_view_has_correct_classes(self, app, sample_table_data):
        """Test that mobile view uses correct Bootstrap visibility classes."""
        template = """
        {% from 'generic_table.html.jinja' import generic_table %}
        {{ generic_table(table_data) }}
        """
        
        with app.test_request_context():
            rendered = render_template_string(template, table_data=sample_table_data)
            soup = BeautifulSoup(rendered, 'html.parser')
            
            mobile = soup.find('div', class_='card-container')
            assert 'd-block' in mobile.get('class')  # Visible on small screens
            assert 'd-md-none' in mobile.get('class')  # Hidden on medium+
