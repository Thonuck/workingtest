import pytest
from flask import render_template_string

INPUT_TEMPLATE = """
{% from "details_screen.html.jinja" import wt_text_field, wt_date_field %}
{{ wt_text_field(name, label=label, edit=edit) }}
"""

DATE_INPUT_TEMPLATE = """
{% from "details_screen.html.jinja" import wt_date_field %}
{{ wt_date_field(name, label=label, edit=edit) }}
"""

SELECT_FIELD_TEMPLATE = """
{% from "details_screen.html.jinja" import wt_select_field %}
{{ wt_select_field(name, label=label, options=options, edit=edit) }}
"""


def test_input_macro_view(app):
    with app.app_context():
        html = render_template_string(INPUT_TEMPLATE, name="Hallo!", label="Test Label", edit=False)
        assert "input type" not in html

def test_input_macro_edit(app):
    with app.app_context():
        html = render_template_string(INPUT_TEMPLATE, name="Hallo!", label="Input Feld", edit=True)
        assert "input type" in html

def test_date_input_macro_view(app):
    with app.app_context():
        html = render_template_string(DATE_INPUT_TEMPLATE, name="Hallo!", label="Test Label", edit=False)
        assert 'input type="date"' not in html

def test_select_input_macro_view(app):
    with app.app_context():
        options = [("a", "aber"), ("b", "bello"), ("c", "chello")]
        html = render_template_string(SELECT_FIELD_TEMPLATE, name="Hallo!", label="Test Label", options=options, edit=False)
        assert 'input type="date"' not in html

