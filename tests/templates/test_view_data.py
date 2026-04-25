import pytest
from flask import render_template_string

SELECT_DATA_VIEW_TEMPLATE = """
{% from "details_screen.html.jinja" import wt_data_view %}
{{ wt_data_view(view_data=view_data) }}
"""

def test_view_data_macro(app):
    with app.app_context():
        view_data = {"fields": [{"type": "text",
                                 "name": "name",
                                 "label": "Vorname",
                                 "value": "Bert",
                                 "required": True},
                                {"type": "text",
                                 "name": "name",
                                 "label": "Vorname",
                                 "value": "Chello",
                                 "required": True},
                                {"type": "date",
                                 "name": "wt_date",
                                 "label": "Datum",
                                 "value": "2026-03-31",
                                 "required": True},
                                {"type": "select",
                                 "name": "wt_role",
                                 "label": "Rolle",
                                 "options": [("besucher", "Besucher"), ("helfer", "Helfer"), ("stuart", "Stuart"), ("richter", "Richter")],
                                 "value": "besucher",
                                 "required": True},
                               ],
                     "edit": False}

        html = render_template_string(SELECT_DATA_VIEW_TEMPLATE, view_data=view_data)
        print(html)
