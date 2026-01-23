Pages of the workingtest app:

## Overview

The application consists of the following main pages organized into blueprints:
- **main**: index, about
- **users**: login, register, user management
- **wts**: create and manage working tests
- **exercises**: exercise management and results (dedicated blueprint for exercise-related pages)

---

## Core Pages

### Index Page (`/`)

**Blueprint**: main  
**Route**: `@bp.route('/')`

Displays a list of all working tests/competitions.

**Features**:
- Shows all active competitions with details (name, level, location, date)
- Indicates if results are published or not
- Different actions available depending on user role:
  - **Admin/Organizer**: Can create new working tests, view full details, manage exercises
  - **Helper**: Can see exercises assigned to them
  - **Visitor**: Can only view published results (if available)

**Access**: Public (all authenticated users + guests)

---

### Working Test Details (`/wts/details/<competition_id>`)

**Blueprint**: wts  
**Route**: `@bp.route('/wts/details/<int:competition_id>')`

Contains the details of a working test/competition.

**Features**:
- Display competition information (name, level, location, date)
- Link to exercises screen
- Link to results screen
- (Can be enhanced with admin/organizer options)

**Access**: All authenticated users

---

## Exercise Management Pages

All exercise-related pages are under the **exercises** blueprint (`/exercises/`).

### WT Exercises Page (`/exercises/wt/<competition_id>`)

**Route**: `@bp.route('/exercises/wt/<int:competition_id>')`

Displays a table of all exercises for a specific working test.

**Features**:
- Table with columns: Exercise Name, Max Points, Judge, Helper, Actions
- Initially empty (no exercises exist)
- Action buttons for each exercise:
  - "Points" button to enter/view points
  - "Edit" button (admin/organizer only)
  - "Delete" button (admin/organizer only)
- "Add Exercise" button (admin/organizer only)
- "View Results" button (admin/organizer only)

**Role-based Access**:
- **Admin/Organizer**: See all exercises, can add/edit/delete
- **Helper**: See only exercises assigned to them
- **Visitor/Guest**: 403 Forbidden (not allowed)

**Access Control**: login_required, roles_required(['admin', 'organizer', 'helper'])

---

### Add Exercise Page (`/exercises/add/<competition_id>`)

**Route**: `@bp.route('/exercises/add/<int:competition_id>', methods=['GET', 'POST'])`

Form to create a new exercise for a working test.

**Features**:
- Input field: Exercise Name (required)
- Input field: Max Points (default: 100)
- Dropdown: Assign Judge (optional, for judges/admins/organizers)
- Dropdown: Assign Helper (optional, for helpers/admins/organizers)
- Submit button creates the exercise and redirects to exercises list

**Access**: Admin/Organizer only

---

### Edit Exercise Page (`/exercises/edit/<exercise_id>`)

**Route**: `@bp.route('/exercises/edit/<int:exercise_id>', methods=['GET', 'POST'])`

Form to modify an existing exercise.

**Features**:
- Pre-filled form with current exercise details
- Can change name, max points, judge, and helper assignments
- Updates exercise and redirects to exercises list

**Access**: Admin/Organizer only

---

### Delete Exercise (`/exercises/delete/<exercise_id>`)

**Route**: `@bp.route('/exercises/delete/<int:exercise_id>', methods=['POST'])`

Deletes an exercise and all associated data (point entries and results).

**Features**:
- Confirmation dialog on the frontend
- Cascading deletion of related point entries and results
- Redirects to exercises list

**Access**: Admin/Organizer only

---

## Point Entry Page (`/exercises/point-entry/<exercise_id>`)

**Route**: `@bp.route('/exercises/point-entry/<int:exercise_id>', methods=['GET', 'POST'])`

The place where helpers enter points for each starter in an exercise.

**Features**:
- Table with columns: Starter, Points Input Field (0 to max_points), Notes
- One row per starter participating in the competition
- Point entry validation (must be between 0 and max points)
- Optional notes field for each starter
- Save button persists all entries to database
- Last updated timestamp tracking

**Role-based Access**:
- **Helper assigned to exercise**: Full access
- **Admin/Organizer**: Full access to all exercises
- **Other helpers/visitors**: 403 Forbidden

**Access Control**: login_required, authorization check for helper assignment

---

## Results Page (`/exercises/results/<competition_id>`)

**Route**: `@bp.route('/exercises/results/<int:competition_id>')`

The final results/leaderboard screen for an entire working test.

**Features**:
- **Ranking Table** with columns:
  - Ranking (with medals for top 3: 🥇🥈🥉)
  - Starter (person name + dog name)
  - Individual scores for each exercise
  - Total points (highlighted badge)
- Results are sorted by total points (descending)
- Publication status indicator (Published/Not Published)
- **Admin/Organizer Actions**:
  - Publish Results button: Makes results visible to visitors
  - Unpublish Results button: Hides results from public view
  - Publish timestamp tracking

**Display Rules**:
- **Organizer/Admin**: Always see the full results page and can publish/unpublish
- **Visitor/Helper**: Can see if published (from index page), otherwise no access

**Access Control**: login_required, roles_required(['admin', 'organizer'])

---

## Publish/Unpublish Results

**Routes**:
- `@bp.route('/exercises/publish/<int:competition_id>', methods=['POST'])`
- `@bp.route('/exercises/unpublish/<int:competition_id>', methods=['POST'])`

Actions for publishing and unpublishing competition results.

**Features**:
- Sets publication status in database
- Records publication timestamp
- Updates availability for visitors on index page
- Flash messages confirming action

**Access**: Admin/Organizer only

---

## User Roles and Access Control

The application implements the following user roles with specific access levels:

| Role | Can Create WTs | Can Manage Exercises | Can Enter Points | Can View Results | Can Publish Results |
|------|---|---|---|---|---|
| Admin | ✓ | ✓ | ✓ | ✓ | ✓ |
| Organizer | ✓ | ✓ | ✓ | ✓ | ✓ |
| Helper | ✗ | ✗ | ✓* | ✓** | ✗ |
| Visitor/Guest | ✗ | ✗ | ✗ | ✓** | ✗ |

\* Only for assigned exercises  
\*\* Only if results are published