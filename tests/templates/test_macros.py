import pytest
from flask import render_template_string

SELCT_FIELD_TEMPLATE = """
{% from "generic_details.html.jinja" import select_field %}
{{ select_field(name=name, label=label, options=options) }}
"""

TEXTAREA_FIELD_TEMPLATE = """
{% from "generic_details.html.jinja" import textarea_field %}
{{ textarea_field(name=name, label=label, value=value) }}
"""

INPUT_FIELD_TEMPLATE = """
{% from "generic_details.html.jinja" import input_field %}
{{ input_field(name=name, label=label, value=value) }}
"""

DETAIL_VIEW_TEMPLATE = """
{% from "generic_details.html.jinja" import input_field %}
"""


def test_macro_select_field(app):
    with app.app_context():
        options = {"eins": "Hello", "zwei": "World"}
        rendered: str = render_template_string(
            source=SELCT_FIELD_TEMPLATE, options=options, name="test", label="Test"
        )
        print(rendered)


def test_macro_textarea_field(app):
    with app.app_context():
        rendered: str = render_template_string(
            source=TEXTAREA_FIELD_TEMPLATE,
            value="Hello World",
            name="name_test",
            label="label_test",
        )

        assert "textarea" in rendered
        assert "Hello World" in rendered


def test_macro_input_field(app):
    with app.app_context():
        rendered: str = render_template_string(
            source=INPUT_FIELD_TEMPLATE, value="Hello World", name="test", label="Test"
        )

        assert "input" in rendered
        assert "Hello World" in rendered


def test_generic_details_view(app):
    with app.app_context():
        rendered: str = render_template_string(
            source=INPUT_FIELD_TEMPLATE, value="Hello World", name="test", label="Test"
        )
