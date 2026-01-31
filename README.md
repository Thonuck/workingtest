Webpage for Dog Competitions
============================

The main screen shows an overview of all competitions:

| Competition | Degree | Location | Date |

---

## Installation und Setup

### Erste Installation

1. **Abhängigkeiten installieren:**
```bash
pip install -r requirements.txt
```

2. **Datenbank initialisieren:**
```bash
python reset_database.py
```

Dies erstellt die Datenbank mit dem aktuellen Schema und einem Admin-User:
- **Username:** admin
- **Password:** admin

3. **Anwendung starten:**
```bash
python run.py
```

Die Anwendung ist dann unter `http://127.0.0.1:5000` erreichbar.

### Fehlerbehebung: Database Schema Fehler

**Problem:** `sqlalchemy.exc.OperationalError: no such column: user.password_hash`

**Ursache:** Die Datenbank verwendet ein altes Schema, das nicht mit dem aktuellen Code kompatibel ist.

**Lösung 1 (Empfohlen für Entwicklung):**
```bash
python reset_database.py
```
⚠️ **WARNUNG:** Löscht alle Daten!

**Lösung 2 (Manuell):**
```bash
# Alte Datenbank löschen
rm instance/database.db

# Anwendung neu starten (erstellt automatisch neue Datenbank)
python run.py
```

**Lösung 3 (Für Produktion mit Datenerhalt):**
Falls Produktionsdaten erhalten bleiben müssen, kontaktieren Sie den Projektbetreuer für eine Migrations-Strategie.

**Best Practice:** Verwenden Sie Flask-Migrate für zukünftige Schema-Änderungen!

---

## Template Macros Documentation

### Overview

The application provides a comprehensive set of Jinja2 macros for building consistent, responsive UI components. Macros are organized into five categories:

1. **Layout Macros** - Page structure and headers
2. **Form Macros** - Form components and inputs
3. **Table Macros** - Data tables and table components
4. **UI Component Macros** - Buttons, badges, alerts, etc.
5. **Legacy Macros** - Deprecated macros for backward compatibility

### Quick Start

Import macros from their respective files:

```jinja
{% from "macros/layout.html.jinja" import page_header %}
{% from "macros/forms.html.jinja" import form_section, input_field %}
{% from "macros/tables.html.jinja" import data_table, table_row %}
{% from "macros/ui.html.jinja" import alert_box, status_badge %}
```

Or use the unified macros file:

```jinja
{% from "macros.html.jinja" import page_header, form_section, data_table %}
```

---

### 1. Layout Macros

#### `page_header(title, subtitle='', level='', location='', date='')`

Creates a page header with title, optional subtitle, and metadata.

**Example - Simple header:**
```jinja
{% from "macros/layout.html.jinja" import page_header %}
{{ page_header(title="Competition Results") }}
```

**Example - Header with metadata:**
```jinja
{{ page_header(
    title="Working Test 2024",
    subtitle="Annual Dog Competition",
    level="Advanced (F)",
    location="Berlin",
    date="2024-03-15"
) }}
```

**Example - Header with action buttons:**
```jinja
{% call page_header(title="My Competitions") %}
    <a href="{{ url_for('wts.create') }}" class="btn btn-primary">Create New</a>
{% endcall %}
```

---

### 2. Form Macros

#### `form_section(title, action_url='', method='POST', submit_label='Submit', cancel_url='', show_flash=true)`

Creates a centered form container with title, flash messages, and buttons.

**Example:**
```jinja
{% from "macros/forms.html.jinja" import form_section, input_field, select_field %}

{% call form_section(
    title="Create Competition",
    action_url=url_for('wts.create'),
    submit_label="Create",
    cancel_url=url_for('wts.index')
) %}
    {{ input_field(name="name", label="Competition Name", required=true) }}
    {{ input_field(name="location", label="Location", required=true) }}
    {{ input_field(name="date", label="Date", type="date", required=true) }}
    {{ select_field(
        name="level",
        label="Level",
        options=[('A', 'Beginner'), ('F', 'Advanced'), ('O', 'Open')],
        required=true
    ) }}
{% endcall %}
```

#### `input_field(name, label, value='', type='text', required=false, min=none, max=none, placeholder='')`

Creates a Bootstrap 5 styled input field.

**Examples:**
```jinja
{# Text input #}
{{ input_field(name="email", label="Email", type="email", required=true) }}

{# Number input with constraints #}
{{ input_field(
    name="score",
    label="Score",
    type="number",
    min=0,
    max=20,
    placeholder="Enter score (0-20)"
) }}

{# Date input #}
{{ input_field(name="date", label="Competition Date", type="date", value="2024-03-15") }}
```

#### `select_field(name, label, options, selected='', required=false, empty_option='-- Select --')`

Creates a dropdown select field.

**Example:**
```jinja
{{ select_field(
    name="helper_id",
    label="Assign Helper",
    options=[(h.id, h.name) for h in helpers],
    selected=exercise.helper_id,
    required=true
) }}
```

#### `textarea_field(name, label, value='', placeholder='', required=false, rows=3)`

Creates a multi-line text input.

**Example:**
```jinja
{{ textarea_field(
    name="description",
    label="Competition Description",
    placeholder="Enter a detailed description...",
    rows=5
) }}
```

---

### 3. Table Macros

#### `data_table(headers=[])`

Creates a responsive Bootstrap table with striped rows and dark header.

**Example - Basic table:**
```jinja
{% from "macros/tables.html.jinja" import data_table %}

{% call data_table(headers=["Name", "Level", "Location", "Date"]) %}
    {% for comp in competitions %}
    <tr>
        <td>{{ comp.name }}</td>
        <td>{{ comp.level }}</td>
        <td>{{ comp.location }}</td>
        <td>{{ comp.date }}</td>
    </tr>
    {% endfor %}
{% endcall %}
```

#### `table_row(url)`

Makes an entire table row clickable.

**Example - Table with clickable rows:**
```jinja
{% from "macros/tables.html.jinja" import data_table, table_row %}

{% call data_table(headers=["Competition", "Date", "Status"]) %}
    {% for comp in competitions %}
        {% call table_row(url=url_for('wts.wt_details', competition_id=comp.id)) %}
            <td>{{ comp.name }}</td>
            <td>{{ comp.date }}</td>
            <td>{{ comp.status }}</td>
        {% endcall %}
    {% endfor %}
{% endcall %}
```

#### `action_buttons(buttons=[])`

Creates a button group for table row actions.

**Example:**
```jinja
{% from "macros/tables.html.jinja" import data_table, action_buttons %}

{% call data_table(headers=["Exercise", "Helper", "Actions"]) %}
    {% for exercise in exercises %}
    <tr>
        <td>{{ exercise.name }}</td>
        <td>{{ exercise.helper.name }}</td>
        <td>
            {{ action_buttons([
                {
                    'type': 'link',
                    'label': 'Edit',
                    'url': url_for('exercises.edit', id=exercise.id),
                    'style': 'info'
                },
                {
                    'type': 'submit',
                    'label': 'Delete',
                    'url': url_for('exercises.delete', id=exercise.id),
                    'style': 'danger',
                    'confirm': 'Delete this exercise?'
                }
            ]) }}
        </td>
    </tr>
    {% endfor %}
{% endcall %}
```

---

### 4. UI Component Macros

#### `flash_messages()`

Displays Flask flash messages with Bootstrap alert styling.

**Example:**
```jinja
{% from "macros/ui.html.jinja" import flash_messages %}
{{ flash_messages() }}
```

#### `alert_box(message, type='info', title='')`

Creates a Bootstrap alert box.

**Examples:**
```jinja
{% from "macros/ui.html.jinja" import alert_box %}

{# Success message #}
{{ alert_box(message="Competition created successfully!", type="success") }}

{# Warning with title #}
{{ alert_box(
    title="Important Notice",
    message="The competition deadline is approaching.",
    type="warning"
) }}
```

#### `empty_state(title, message, action_url='', action_label='')`

Shows a message when no data is available.

**Examples:**
```jinja
{% from "macros/ui.html.jinja" import empty_state %}

{# Simple empty state #}
{{ empty_state(
    title="No Competitions Found",
    message="There are currently no competitions scheduled."
) }}

{# With action button #}
{{ empty_state(
    title="No Exercises Assigned",
    message="This competition has no exercises yet.",
    action_url=url_for('exercises.create', competition_id=comp.id),
    action_label="Create First Exercise"
) }}
```

#### `button_group(buttons=[])`

Creates a horizontal group of buttons.

**Example:**
```jinja
{% from "macros/ui.html.jinja" import button_group %}

{{ button_group([
    {'type': 'link', 'label': 'Back', 'url': url_for('wts.index'), 'style': 'secondary'},
    {'type': 'link', 'label': 'Edit', 'url': url_for('wts.edit', id=comp.id), 'style': 'primary'},
    {
        'type': 'form',
        'label': 'Delete',
        'url': url_for('wts.delete', id=comp.id),
        'style': 'danger',
        'confirm': 'Are you sure?'
    }
]) }}
```

#### `status_badge(published, published_label='Published', unpublished_label='Not Published')`

Displays a colored status badge.

**Examples:**
```jinja
{% from "macros/ui.html.jinja" import status_badge %}

{{ status_badge(published=competition.is_published) }}

{# Custom labels #}
{{ status_badge(
    published=user.is_active,
    published_label='Active',
    unpublished_label='Inactive'
) }}
```

#### `ranking_badge(rank)`

Displays ranking with medal emojis for top 3 positions.

**Example:**
```jinja
{% from "macros/ui.html.jinja" import ranking_badge %}

<table>
    <tr>
        <td>{{ ranking_badge(rank=1) }}</td>  {# Shows: 🥇 1st #}
        <td>Max & Bella</td>
        <td>95 points</td>
    </tr>
    <tr>
        <td>{{ ranking_badge(rank=2) }}</td>  {# Shows: 🥈 2nd #}
        <td>Anna & Rex</td>
        <td>89 points</td>
    </tr>
</table>
```

---

### Complete Page Example

Here's a complete example combining multiple macros:

```jinja
{% extends "base.html" %}
{% from "macros/layout.html.jinja" import page_header %}
{% from "macros/tables.html.jinja" import data_table, table_row, action_buttons %}
{% from "macros/ui.html.jinja" import empty_state, status_badge %}

{% block content %}
{% call page_header(title="Competitions", subtitle="Manage all competitions") %}
    <a href="{{ url_for('wts.create') }}" class="btn btn-primary">Create New</a>
{% endcall %}

{% if competitions %}
    {% call data_table(headers=["Name", "Level", "Date", "Status", "Actions"]) %}
        {% for comp in competitions %}
            <tr>
                <td>{{ comp.name }}</td>
                <td>{{ comp.level }}</td>
                <td>{{ comp.date }}</td>
                <td>{{ status_badge(published=comp.is_published) }}</td>
                <td>
                    {{ action_buttons([
                        {'type': 'link', 'label': 'View', 'url': url_for('wts.detail', id=comp.id), 'style': 'info'},
                        {'type': 'link', 'label': 'Edit', 'url': url_for('wts.edit', id=comp.id), 'style': 'primary'}
                    ]) }}
                </td>
            </tr>
        {% endfor %}
    {% endcall %}
{% else %}
    {{ empty_state(
        title="No Competitions Yet",
        message="Get started by creating your first competition.",
        action_url=url_for('wts.create'),
        action_label="Create Competition"
    ) }}
{% endif %}
{% endblock %}
```

---

## Frontend Development Guidelines

### Responsive Design Best Practices

**⚠️ WICHTIG: Alle HTML-Templates MÜSSEN für PC, Tablet und Handy optimiert sein!**

#### Warum Responsive Design?
- **Nutzerfreundlichkeit**: Viele Nutzer greifen mobil auf die Anwendung zu
- **Professionelles Erscheinungsbild**: Mobile-First ist heute Standard
- **Bessere Wartbarkeit**: Einheitliche Darstellung auf allen Geräten

#### Implementierte Responsive Features:

##### 1. **Tabellen (z.B. Competition-Übersicht)**
```html
<!-- FALSCH - nicht responsive -->
<table>...</table>

<!-- RICHTIG - responsive -->
<div class="table-responsive">
    <table class="table table-striped table-hover">...</table>
</div>
```
**Warum?** Tabellen werden auf kleinen Bildschirmen horizontal scrollbar und brechen nicht das Layout.

**Zusätzlich**: Spalten können auf Handy ausgeblendet werden:
```html
<th class="d-none d-md-table-cell">Date</th>  <!-- Nur ab Tablet sichtbar -->
```

##### 2. **Bootstrap Grid System**
```html
<!-- FALSCH - funktioniert nur auf Desktop -->
<div class="col-md-6 offset-md-3">

<!-- RICHTIG - funktioniert auf allen Geräten -->
<div class="col-12 col-sm-10 col-md-8 col-lg-6 offset-sm-1 offset-md-2 offset-lg-3">
```

**Breakpoints:**
- `col-12`: Handy (100% Breite)
- `col-sm-10`: Kleine Tablets (83% Breite)
- `col-md-8`: Tablets (66% Breite)
- `col-lg-6`: Desktop (50% Breite)

**Warum?** Formulare sind auf Handys zu schmal und schwer bedienbar ohne diese Anpassungen.

##### 3. **Navigation**
- Verwendet `flex-wrap` für automatisches Umbrechen auf kleinen Bildschirmen
- Navigation stapelt sich vertikal auf Handys (siehe `custom.css`)

##### 4. **Viewport Meta-Tag** (PFLICHT!)
```html
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
```
**Warum?** Ohne diesen Tag wird die Seite auf mobilen Geräten falsch skaliert!

### Zentrale CSS-Verwaltung

**Datei: `/app/static/custom.css`**

Alle projektspezifischen Styles MÜSSEN in dieser zentralen Datei definiert werden:

**Warum zentrale CSS-Datei?**
- ✅ **Konsistenz**: Alle Seiten haben dasselbe Look & Feel
- ✅ **Wartbarkeit**: Änderungen nur an einer Stelle
- ✅ **Performance**: CSS wird gecacht vom Browser
- ✅ **Übersichtlichkeit**: Keine inline-styles in HTML-Templates

**Einbindung in base.html:**
```html
<link rel="stylesheet" href="{{ url_for('static', filename='custom.css') }}">
```

**Inhalt von custom.css:**
- Responsive Media Queries für alle Breakpoints
- Mobile-First CSS-Regeln
- Konsistente Button- und Form-Styles
- Tabellen-Optimierungen

### Template-Struktur

**Datei: `/app/templates/base.html`**

**Alle HTML-Templates MÜSSEN `base.html` erweitern!**

```html
{% extends "base.html" %}
{% block content %}
    <!-- Ihr Inhalt -->
{% endblock %}
```

**Warum?**
- ✅ Navigation ist überall konsistent
- ✅ Login/Logout-Status wird automatisch angezeigt
- ✅ Bootstrap und custom.css sind überall verfügbar
- ✅ Änderungen an der Navigation müssen nur einmal gemacht werden

**❌ NICHT:** Separate base.html in jedem Blueprint-Ordner erstellen!

### Checkliste für neue HTML-Templates:

- [ ] `{% extends "base.html" %}` am Anfang
- [ ] Bootstrap Grid System verwenden (`row`, `col-*`)
- [ ] Tabellen in `<div class="table-responsive">` wrappen
- [ ] Responsive Breakpoints definieren (col-12, col-sm-, col-md-, col-lg-)
- [ ] Styles in `custom.css` definieren, nicht inline
- [ ] Auf Handy, Tablet und Desktop testen

---

### Competition Degrees
There are three degrees for dog competitions:
- **A (Beginner)**: For new participants.
- **F (Advanced)**: For experienced participants.
- **O (Open)**: Open to all participants.

### User Roles and Permissions

#### Everybody (Guest)
- Can view the competition table and select a competition.
- Can view the results of a competition (results are anonymized and show only starter numbers).

#### Organizer (Logged In)
- Can view the competition table.
- Can create a new competition.
- Can open and configure competitions they own, including assigning judges, helpers, and exercises.

#### Helper (Logged In)
- Can view all competitions.
- Has two views for a competition:
  - **Result View**: View results of a competition.
  - **Helper View**: Enter results for exercises they are assigned to.

---

### Competition Workflow
Each competition is executed as follows:
1. **Roles**: 
   - One organizer.
   - Several judges and helpers.
2. **Duration**: Typically runs for half a day.
3. **Exercises**: Each starter completes around 5 exercises.
4. **Judging**:
   - Judges evaluate starters and their dogs on each exercise.
   - Scores range from 0 (not passed) to 20 (excellent).
   - Judges communicate final scores to helpers, who enter them into the application.
5. **Grouping**:
   - Starters are divided into groups to ensure smooth parallel execution.
6. **Results**:
   - Scores from all exercises are aggregated to determine the top three starters.
   - Results are published with starter numbers only (no names).

---

### Competition Configuration

#### General Information
Each competition includes:
- **Competition Name**
- **Competition Level** (A, F, or O)
- **Location**
- **Date**

#### Judges
| Given Name | Family Name | Email | Exercises |
- Judges are assigned specific exercises to evaluate.

#### Helpers
| Given Name | Family Name | Email | Exercises | Judge-Helper |
- Helpers are assigned specific exercises.
- Judge-helpers receive login credentials to enter results for their assigned exercises.
- Helpers see:
  - Exercise number.
  - List of starter numbers (grouped for easier navigation).
  - Input fields for entering scores.

#### Starters
A starter is a person with a dog. Starter details:
| Starter Number | Person ID | Dog ID | Paid | Present |
- Starter numbers are unique per competition and formatted as:
  - A1, A2, A3... for Level A.
  - F1, F2, F3... for Level F.
  - O1, O2, O3... for Level O.

#### Person
| Person ID | Given Name | Family Name | Email |

#### Dog
| Dog ID | Dog Name | Dog Breed | Kennel |

#### Exercises
| Exercise ID | Judge ID | Helper ID | Exercise Name |
- Exercise names are typically "Task 1", "Task 2", ..., "Task 5".

---

### Helper Result Entry
Helpers maintain a result table for their assigned exercises. The result entry page includes:
- **Exercise Number**: Displayed at the top.
- **Starter List**: Grouped by starter numbers.
- **Score Input**: Fields to enter scores for each starter.

Example:
| Starter Number | Result |
|----------------|--------|
| A1             | 18     |
| A2             | 15     |
| A3             | 20     |

---

# Updated application structure for modularization and maintainability

# Application Skeleton

The application is structured as follows:

```
workingtest_webapp/
    workingtest/
        config.py          # Configuration settings (e.g., database URI, secret keys)
        extensions.py      # Extensions initialization (e.g., SQLAlchemy, Flask-Migrate)
        flask_app.py       # Main entry point for the Flask app
        models.py          # SQLAlchemy models
        README.md          # Project documentation

        blueprints/        # Blueprints for modularization
            __init__.py    # Blueprint registration
            main/          # Main blueprint for public views
                __init__.py
                routes.py  # Routes for main views (e.g., competition table)
                forms.py   # WTForms for main views
                templates/ # Templates for main views
                    ...
            organizer/     # Blueprint for organizer-specific views
                __init__.py
                routes.py  # Routes for organizer views (e.g., competition configuration)
                forms.py   # WTForms for organizer views
                templates/ # Templates for organizer views
                    ...
            helper/        # Blueprint for helper-specific views
                __init__.py
                routes.py  # Routes for helper views (e.g., result entry)
                forms.py   # WTForms for helper views
                templates/ # Templates for helper views
                    ...

        static/            # Static files (CSS, JS, images)
            style.css

        templates/         # Shared templates (e.g., base.html)
            base.html
            ...

        migrations/        # Flask-Migrate files for database migrations
```

This structure ensures modularity and maintainability of the application.

# Create the route for the main index. "/"
- Add route in main/routes.py to template main/templates/index.html
- create index.html

### Implementing the Context for the Main Screen in `index.html`

To implement the context for the main screen in `index.html`, follow these steps:

1. **Define the Purpose**:
   - The main screen should display an overview of all competitions in a table format.
   - Include columns for `Competition`, `Degree`, `Location`, and `Date`.

2. **Set Up the Route**:
   - In `main/routes.py`, create a route for the main screen (e.g., `/` or `/index`).
   - Fetch the necessary data (e.g., competitions) from the database and pass it to the template.

3. **Create the Template Skeleton**:
   - Use the `index.html` file in the `templates/` directory.
   - Extend the `base.html` template to maintain a consistent layout.
   - Add a table structure to display the competition data.

4. **First Skeleton for `index.html`**:

```html
{% extends "base.html" %}

{% block content %}
<div class="container">
    <h1>Competitions Overview</h1>
    <table class="table">
        <thead>
            <tr>
                <th>Competition</th>
                <th>Degree</th>
                <th>Location</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody>
            <!-- Loop through competitions and display them -->
            {% for competition in competitions %}
            <tr>
                <td>{{ competition.name }}</td>
                <td>{{ competition.degree }}</td>
                <td>{{ competition.location }}</td>
                <td>{{ competition.date }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

5. **Style the Table**:
   - Use the `style.css` file in the `static/` directory to style the table and ensure it is visually appealing.

6. **Test the Implementation**:
   - Run the application and navigate to the main screen to verify that the competition data is displayed correctly.


