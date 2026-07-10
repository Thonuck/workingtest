# Unit Testing Jinja Templates - Guide and Examples

This document provides comprehensive guidance on unit testing Jinja templates in Flask applications, with specific examples from the `generic_table.html.jinja` template.

## Table of Contents

1. [Approaches to Testing Jinja Templates](#approaches-to-testing-jinja-templates)
2. [Implementation Example](#implementation-example)
3. [Best Practices](#best-practices)
4. [Running the Tests](#running-the-tests)

## Approaches to Testing Jinja Templates

### 1. Direct Template Rendering (Recommended) ⭐

**Description:** Render templates directly with mock data and assert on the HTML output using HTML parsing libraries.

**Pros:**
- Fast execution
- Tests template logic in isolation
- Easy to set up test data
- No HTTP overhead
- Can test individual macros in isolation

**Cons:**
- Need to parse HTML for assertions (requires BeautifulSoup or similar)
- May miss integration issues with Flask context

**Example:**
```python
def test_flash_messages_displays_single_message(app):
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
```

### 2. Integration Testing via Flask Test Client

**Description:** Test templates through complete Flask routes using the test client.

**Pros:**
- Tests full request cycle including URL routing
- Catches integration issues
- Tests context preparation in view functions
- More realistic end-to-end testing

**Cons:**
- Slower execution
- Harder to isolate template-specific issues
- More setup required
- Couples template tests to route logic

**Example:**
```python
def test_index_page_displays_competitions(client):
    # Assumes a route exists that uses generic_table
    response = client.get('/competitions')
    assert response.status_code == 200
    assert b'Competition Table' in response.data
```

### 3. Snapshot Testing

**Description:** Compare rendered output against saved "golden" snapshots to detect unintended changes.

**Pros:**
- Catches unintended visual/structural changes
- Good for regression testing
- Less manual assertion writing

**Cons:**
- Can be brittle with frequent legitimate changes
- Requires manual review of snapshot updates
- Large snapshot files can be hard to review
- May miss logical errors if snapshot is wrong

**Example:**
```python
def test_table_snapshot(app, snapshot):
    """Would use pytest-snapshot or similar"""
    rendered = render_template('generic_table.html.jinja', table_data=data)
    snapshot.assert_match(rendered, 'generic_table_output.html')
```

### 4. Macro-Level Testing (Used in this Project) ⭐

**Description:** Test individual Jinja macros in isolation with focused test cases.

**Pros:**
- Tests reusable components separately
- Catches macro-specific bugs early
- Fast and focused
- Easy to understand failures
- Great for component libraries

**Cons:**
- Requires careful setup of macro context
- Need to understand macro parameter structure
- Must test macro compositions separately

**Example:**
```python
def test_clickable_row_has_onclick_handler(app):
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
        assert row.get('onclick') == "window.location='/test/url'"
        assert 'cursor: pointer' in row.get('style')
```

## Implementation Example

The test suite for `generic_table.html.jinja` demonstrates **macro-level unit testing** with the following structure:

### Test Organization

```
tests/templates/
├── __init__.py
└── test_generic_table.py
```

### Key Components Tested

1. **Flash Messages Macro** - Tests alert rendering
2. **Normal Table Macro** - Tests table structure creation
3. **Clickable Table Row Macro** - Tests onclick handlers
4. **Card List Macro** - Tests mobile card layout
5. **Generic Wide Table Macro** - Tests desktop table view
6. **Generic Table Macro** - Tests complete responsive table
7. **Data Structure Validation** - Tests required fields
8. **Responsiveness** - Tests Bootstrap visibility classes

### Example Test Structure

```python
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
```

### Test Fixtures

```python
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
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ],
        "details_route": "wts.wt_details"
    }
```

## Best Practices

### 1. Test Template Logic, Not Presentation

Focus on testing:
- Conditional rendering (`{% if %}`)
- Loops (`{% for %}`)
- Variable substitution
- Macro parameter handling
- Error states (empty data, missing fields)

Avoid testing:
- Exact CSS classes (unless critical for functionality)
- Precise HTML formatting
- Whitespace and indentation

### 2. Use BeautifulSoup for HTML Parsing

BeautifulSoup provides robust HTML parsing that handles imperfect HTML:

```python
soup = BeautifulSoup(rendered, 'html.parser')

# Find elements
alert = soup.find('div', class_='alert')
cards = soup.find_all('div', class_='card')

# Check attributes
assert 'onclick' in row.attrs
assert 'cursor: pointer' in row.get('style')

# Check text content
assert 'Expected text' in element.text
```

### 3. Test Edge Cases

Always test:
- Empty data lists
- Missing optional parameters
- Invalid route names
- Null/None values
- Special characters in data

```python
def test_generic_table_handles_empty_data(app, empty_table_data):
    """Test that generic_table handles empty items gracefully."""
    # ... test implementation
    assert 'Keine Einträge verfügbar' in rendered
```

### 4. Test Both Mobile and Desktop Views

For responsive templates, test visibility classes:

```python
def test_desktop_view_has_correct_classes(app, sample_table_data):
    desktop = soup.find('div', class_='table-container')
    assert 'd-none' in desktop.get('class')  # Hidden on small screens
    assert 'd-md-block' in desktop.get('class')  # Visible on medium+
```

### 5. Organize Tests by Component

Use test classes to group related tests:

```python
class TestFlashMessagesMacro:
    """Tests for the flash_messages macro."""
    # All flash message tests here

class TestCardListMacro:
    """Tests for the card_list macro (mobile view)."""
    # All card list tests here
```

### 6. Use Descriptive Test Names

Test names should explain:
- What is being tested
- What scenario/condition
- Expected outcome

```python
def test_flash_messages_displays_single_message()
def test_card_list_shows_message_for_empty_items()
def test_generic_table_hides_flash_when_disabled()
```

### 7. Pay Attention to Macro Parameter Order

When testing macros, parameters must be passed in the correct order:

```python
# Macro definition
{% macro card_list(title_key, headers, items, details_route, competition_id=None) %}

# Correct test usage - positional arguments
{{ card_list(
    table_data.title,
    table_data.headers,
    table_data['items'],
    table_data.details_route,
    42
) }}

# Incorrect - keyword arguments can conflict with built-ins
{{ card_list(items=table_data.items) }}  # 'items' conflicts with dict.items()
```

### 8. Test with Real Flask Application Context

Use `app.test_request_context()` to provide Flask context for `url_for()`, `flash()`, etc.:

```python
with app.test_request_context():
    flash("Test message", "success")
    rendered = render_template_string(template)
```

### 9. Validate Data Structure Requirements

Test that templates work with expected data structures:

```python
def test_headers_are_tuples_of_key_and_display_name(app):
    """Test that headers follow (key, display_name) tuple structure."""
    table_data = {
        "headers": [
            ("field1", "Field One"),
            ("field2", "Field Two")
        ],
        # ...
    }
    # Verify display names are used, not keys
    assert 'Field One' in rendered
    assert 'Field Two' in rendered
```

## Running the Tests

### Run All Template Tests

```bash
pytest tests/templates/ -v
```

### Run Specific Test Class

```bash
pytest tests/templates/test_generic_table.py::TestFlashMessagesMacro -v
```

### Run Single Test

```bash
pytest tests/templates/test_generic_table.py::TestFlashMessagesMacro::test_flash_messages_displays_single_message -v
```

### Run with Coverage

```bash
pytest tests/templates/ --cov=app/templates --cov-report=html
```

### Run with Detailed Output

```bash
pytest tests/templates/ -vv --tb=short
```

## Dependencies

Add to `requirements.txt`:

```
beautifulsoup4==4.12.3
```

Install:

```bash
pip install beautifulsoup4
```

## Summary

The **macro-level unit testing** approach implemented for `generic_table.html.jinja` provides:

✅ Fast, focused tests for each component  
✅ Clear separation of concerns  
✅ Easy debugging when tests fail  
✅ Comprehensive coverage of template logic  
✅ Documentation of expected behavior  
✅ Regression prevention  

This approach is ideal for reusable template components and maintains the benefits of unit testing while working with Jinja templates.
