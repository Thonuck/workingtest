Webpage for Dog Competitions
============================

The main screen shows an overview of all competitions:

| Competition | Degree | Location | Date |

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


