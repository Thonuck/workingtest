# Selenium Test Case Generation Plan

## Overview

This document outlines a comprehensive plan for generating Selenium test cases for all pages in the workingtest application. The test suite will cover functionality, access control, user roles, and edge cases across the main, users, wts, and exercises blueprints.

## Test Organization Structure

Tests are organized by blueprint and further by functional area:

```
tests/selenium/
├── __init__.robot                      # Centralized suite setup/teardown
├── test_user_login.robot               # ✅ DONE: Login & competition creation
├── test_wt_details_delete.robot        # ✅ DONE: WT details & deletion
├── test_unauthenticated_results.robot  # ✅ DONE: Results page access control
├── test_exercises_management.robot     # TODO: Exercise CRUD operations
├── test_point_entry.robot              # TODO: Point entry functionality
├── test_results_publication.robot      # TODO: Results publish/unpublish
└── test_access_control.robot           # TODO: Role-based access verification
```

---

## Page-by-Page Test Plan

### 1. **Index Page** (`/`) - Main Blueprint
**Status**: Partially covered

#### Existing Tests
- ✅ `test_user_login.robot`: Login and redirect to index
- ✅ `test_user_login.robot`: Display of "Workingtest Planer"

#### Missing Test Cases
- [ ] `test_index_page.robot`
  - [ ] Display all competitions (list view)
  - [ ] Display competition details (name, level, location, date)
  - [ ] Display results publication status
  - [ ] Role-based action buttons visibility:
    - [ ] Admin: See create, view details, manage exercises buttons
    - [ ] Organizer: See create, view details, manage exercises buttons
    - [ ] Helper: See assigned exercises link
    - [ ] Visitor: See published results only
  - [ ] Click on competition to navigate to details
  - [ ] Search/filter functionality (if implemented)
  - [ ] Empty state when no competitions exist

---

### 2. **About Page** (`/about`) - Main Blueprint
**Status**: Not tested

#### Test Cases to Create
- [ ] `test_main_pages.robot`
  - [ ] About page is accessible
  - [ ] About page contains expected content
  - [ ] Navigation back to index works

---

### 3. **Login Page** (`/users/login`) - Users Blueprint
**Status**: Partially covered

#### Existing Tests
- ✅ `test_user_login.robot`: Successful login with admin credentials
- ✅ `test_user_login.robot`: Logout functionality

#### Missing Test Cases
- [ ] `test_user_authentication.robot`
  - [ ] Login page displays login form
  - [ ] Login with invalid credentials shows error message
  - [ ] Login with empty username/password shows validation errors
  - [ ] Remember me functionality (if implemented)
  - [ ] Password reset link (if implemented)
  - [ ] Redirect to login from protected pages
  - [ ] Session management and timeout

---

### 4. **Register Page** (`/users/register`) - Users Blueprint
**Status**: Not tested

#### Test Cases to Create
- [ ] `test_user_registration.robot`
  - [ ] Register page displays registration form
  - [ ] Successfully register new user
  - [ ] Validation: Duplicate username rejected
  - [ ] Validation: Password requirements enforced
  - [ ] Validation: Email format validated (if required)
  - [ ] Registration redirects to login
  - [ ] Newly registered user can login

---

### 5. **User Management** - Users Blueprint
**Status**: Not tested

#### Test Cases to Create
- [ ] `test_user_management.robot`
  - [ ] Admin can view list of users
  - [ ] Admin can view user details
  - [ ] Admin can edit user role
  - [ ] Admin can delete user
  - [ ] Non-admin cannot access user management
  - [ ] User list shows all required columns

---

### 6. **Working Test Details** (`/wts/details/<competition_id>`) - WTS Blueprint
**Status**: Partially covered

#### Existing Tests
- ✅ `test_wt_details_delete.robot`: Display competition details
- ✅ `test_wt_details_delete.robot`: Delete working test

#### Missing Test Cases
- [ ] `test_wt_details_extended.robot`
  - [ ] Access control: Only authenticated users can view
  - [ ] Display all competition information (name, level, location, date)
  - [ ] Link to exercises page works
  - [ ] Link to results page works
  - [ ] Admin-only edit option (if implemented)
  - [ ] Edit competition form (if implemented)
  - [ ] Success message after edit

---

### 7. **Exercise Management** (`/exercises/wt/<competition_id>`) - Exercises Blueprint
**Status**: Not tested

#### Test Cases to Create
- [ ] `test_exercises_management.robot`
  - **Access Control**:
    - [ ] Admin/Organizer can access exercises page
    - [ ] Helper can access exercises page (but only assigned exercises)
    - [ ] Visitor gets 403 Forbidden
    - [ ] Unauthenticated user gets redirected to login
  
  - **Exercise List Display**:
    - [ ] Table displays all columns (Name, Max Points, Judge, Helper, Actions)
    - [ ] Empty state when no exercises exist
    - [ ] Multiple exercises display correctly
  
  - **Action Buttons Visibility**:
    - [ ] Admin/Organizer see: Add, Points, Edit, Delete, View Results buttons
    - [ ] Helper sees only: Points button for assigned exercises
    - [ ] Non-assigned helper doesn't see other exercises
  
  - **Navigation**:
    - [ ] Click "Add Exercise" button navigates to add page
    - [ ] Click "View Results" button navigates to results page
    - [ ] "Back to Overview" link works

---

### 8. **Add Exercise** (`/exercises/add/<competition_id>`) - Exercises Blueprint
**Status**: Not tested

#### Test Cases to Create
- [ ] `test_exercise_add.robot`
  - **Access Control**:
    - [ ] Only Admin/Organizer can access
    - [ ] Helper gets 403 Forbidden
    - [ ] Visitor gets 403 Forbidden
  
  - **Form Validation**:
    - [ ] All form fields are present (Name, Max Points, Judge, Helper)
    - [ ] Exercise name is required
    - [ ] Max points is optional (defaults to 100)
    - [ ] Judge dropdown is optional
    - [ ] Helper dropdown is optional
  
  - **Form Submission**:
    - [ ] Successfully create exercise with required fields only
    - [ ] Successfully create exercise with all fields filled
    - [ ] Exercise name validation (no empty values)
    - [ ] Max points validation (numeric only, positive)
    - [ ] Created exercise appears in exercises list
    - [ ] Success flash message appears
  
  - **Error Handling**:
    - [ ] Form redisplays on validation error
    - [ ] Error messages appear for invalid inputs
    - [ ] Non-existent competition returns 404

---

### 9. **Edit Exercise** (`/exercises/edit/<exercise_id>`) - Exercises Blueprint
**Status**: Not tested

#### Test Cases to Create
- [ ] `test_exercise_edit.robot`
  - **Access Control**:
    - [ ] Only Admin/Organizer can access
    - [ ] Helper gets 403 Forbidden
  
  - **Form Pre-population**:
    - [ ] Form loads with current exercise values
    - [ ] All fields can be modified
  
  - **Form Submission**:
    - [ ] Successfully update exercise name
    - [ ] Successfully update max points
    - [ ] Successfully change judge assignment
    - [ ] Successfully change helper assignment
    - [ ] Changes persist in exercise list
    - [ ] Success flash message appears
  
  - **Error Handling**:
    - [ ] Non-existent exercise returns 404
    - [ ] Validation errors handled properly

---

### 10. **Delete Exercise** (`/exercises/delete/<exercise_id>`) - Exercises Blueprint
**Status**: Not tested

#### Test Cases to Create
- [ ] `test_exercise_delete.robot`
  - **Access Control**:
    - [ ] Only Admin/Organizer can delete
    - [ ] Helper cannot delete
  
  - **Deletion Process**:
    - [ ] Delete button triggers confirmation dialog
    - [ ] Canceling dialog doesn't delete
    - [ ] Confirming dialog deletes exercise
    - [ ] Deleted exercise removed from list
    - [ ] Success flash message appears
    - [ ] Cascading deletion: Point entries deleted
    - [ ] Cascading deletion: Results entries deleted

---

### 11. **Point Entry** (`/exercises/point-entry/<exercise_id>`) - Exercises Blueprint
**Status**: Not tested

#### Test Cases to Create
- [ ] `test_point_entry.robot`
  - **Access Control**:
    - [ ] Assigned helper can access own exercises
    - [ ] Unassigned helper cannot access
    - [ ] Admin/Organizer can access all
    - [ ] Non-authenticated user gets redirect
  
  - **Page Display**:
    - [ ] Table shows all starters
    - [ ] Points column displays correctly
    - [ ] Notes column (optional) displays correctly
    - [ ] Exercise name and max points shown
  
  - **Point Entry**:
    - [ ] Enter valid points (within 0-max range)
    - [ ] Enter invalid points (negative) shows error
    - [ ] Enter invalid points (exceeds max) shows error
    - [ ] Enter non-numeric points shows error
    - [ ] Optional notes field accepts text
    - [ ] Save button persists all entries
    - [ ] Success message appears after save
    - [ ] Page reloads with saved values
  
  - **Edit Existing Points**:
    - [ ] Modify previously entered points
    - [ ] Points update correctly
    - [ ] Update notes with new values
  
  - **Bulk Operations**:
    - [ ] Enter points for all starters at once
    - [ ] Mix of filled and empty entries
    - [ ] Partial saves (some starters skip, some filled)

---

### 12. **Results Page** (`/exercises/results/<competition_id>`) - Exercises Blueprint
**Status**: Partially covered

#### Existing Tests
- ✅ `test_unauthenticated_results.robot`: Unauthenticated access & empty state
- ✅ `test_unauthenticated_results.robot`: Admin can see manage buttons

#### Missing Test Cases
- [ ] `test_results_display.robot`
  - **Access Control**:
    - [ ] Unauthenticated user can view (if published or admin route)
    - [ ] Admin/Organizer can always view
    - [ ] Helper can view if published
  
  - **Empty Results State**:
    - [ ] "No results available yet" displays when no data
    - [ ] Message displays correctly
    - [ ] No ranking table shown
  
  - **Results Display with Data**:
    - [ ] Ranking table displays correctly
    - [ ] Ranking badges (🥇🥈🥉) appear for top 3
    - [ ] Starter names displayed
    - [ ] Dog names displayed
    - [ ] Individual exercise scores shown
    - [ ] Total points highlighted in badge
    - [ ] Results sorted by total points (descending)
    - [ ] All starters included
    - [ ] All exercises included
  
  - **Admin/Organizer Controls**:
    - [ ] Publish Results button visible
    - [ ] Unpublish Results button visible (when published)
    - [ ] Publication status badge shows correct state
  
  - **Visitor/Helper View**:
    - [ ] No publish/unpublish buttons visible
    - [ ] Publication status badge shown
  
  - **Navigation**:
    - [ ] "Back to Exercises" link works
    - [ ] "Back to Overview" link works

---

### 13. **Publish/Unpublish Results** - Exercises Blueprint
**Status**: Not tested

#### Test Cases to Create
- [ ] `test_results_publication.robot`
  - **Publish Results**:
    - [ ] Only Admin/Organizer can publish
    - [ ] Click "Publish Results" button
    - [ ] Button changes to "Unpublish Results"
    - [ ] Publication status updates
    - [ ] Success flash message appears
    - [ ] Results become visible to helpers/visitors
  
  - **Unpublish Results**:
    - [ ] Click "Unpublish Results" button
    - [ ] Button changes back to "Publish Results"
    - [ ] Publication status updates
    - [ ] Success flash message appears
    - [ ] Results hidden from helpers/visitors
  
  - **Timestamp Tracking**:
    - [ ] Publication timestamp recorded
    - [ ] Timestamp displayed on results page
  
  - **Visitor Access After Publish**:
    - [ ] Visitor can view published results
    - [ ] Visitor sees full ranking table
    - [ ] Visitor cannot see unpublish button

---

## Access Control Test Matrix

### Central Access Control Test File
- [ ] `test_access_control.robot`

| Page | Route | Unauthenticated | Admin | Organizer | Helper | Visitor |
|------|-------|---|---|---|---|---|
| Index | `/` | ✓ | ✓ | ✓ | ✓ | ✓ |
| About | `/about` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Login | `/users/login` | ✓ | → / | → / | → / | → / |
| Register | `/users/register` | ✓ | ✓ | ✓ | ✓ | ✓ |
| User Mgmt | `/users/...` | ✗ | ✓ | ✗ | ✗ | ✗ |
| WT Details | `/wts/details/<id>` | ✗ | ✓ | ✓ | ✓ | ✓ |
| Exercises | `/exercises/wt/<id>` | ✗ | ✓ | ✓ | ✓* | ✗ |
| Add Exercise | `/exercises/add/<id>` | ✗ | ✓ | ✓ | ✗ | ✗ |
| Edit Exercise | `/exercises/edit/<id>` | ✗ | ✓ | ✓ | ✗ | ✗ |
| Delete Exercise | `/exercises/delete/<id>` | ✗ | ✓ | ✓ | ✗ | ✗ |
| Point Entry | `/exercises/point-entry/<id>` | ✗ | ✓ | ✓ | ✓** | ✗ |
| Results | `/exercises/results/<id>` | ✓*** | ✓ | ✓ | ✓** | ✓** |

Legend:
- `✓` = Allowed
- `✗` = Forbidden (403)
- `→ /` = Redirects to page
- `*` = Only assigned exercises
- `**` = Only if published
- `***` = No data unless published

---

## Test Data Setup Strategy

### Database State Management
- Use `__init__.robot` centralized setup to:
  - Reset database before suite
  - Create admin user
  - Create test competitions
  - Create test starters
  - Start Flask server

### Test Fixtures
Create separate keywords for common setup:
- `Create Test Competition` - Create a competition with specific details
- `Create Test Starters` - Add starters to competition
- `Create Test Exercises` - Add exercises to competition
- `Create Test Points` - Enter points for exercise
- `Login As Admin` - Login with admin credentials
- `Login As Organizer` - Login with organizer credentials
- `Login As Helper` - Login with helper credentials
- `Login As Visitor` - Login with visitor credentials

---

## Test Execution Strategy

### Phase 1: Foundation (Already Complete)
- ✅ User authentication (login/logout)
- ✅ Competition creation and deletion
- ✅ Access control basics

### Phase 2: Exercise Management (Priority High)
- [ ] Exercise CRUD operations
- [ ] Exercise list display
- [ ] Role-based visibility

### Phase 3: Point Entry & Results (Priority High)
- [ ] Point entry workflow
- [ ] Results display
- [ ] Results publication

### Phase 4: Access Control & Edge Cases (Priority Medium)
- [ ] Complete access matrix verification
- [ ] Error handling
- [ ] Edge cases

### Phase 5: User Management (Priority Low)
- [ ] User registration
- [ ] User management interface
- [ ] Role assignment

---

## Test Naming Convention

All test files follow pattern: `test_<feature_area>.robot`

Test cases follow pattern: `Test <Feature> <Scenario>`

Example:
```robot
*** Test Cases ***
Test Create Exercise Successfully
    [Documentation]    Admin can successfully create new exercise
    ...

Test Delete Exercise Removes Associated Points
    [Documentation]    Deleting exercise cascades to point entries
    ...

Test Helper Cannot Delete Exercise
    [Documentation]    Helper role denied deletion of exercises
    ...
```

---

## CI/CD Integration

### Test Execution
```bash
# Run all tests with TRACE logging
robot -L TRACE tests/selenium/

# Run specific test file
robot tests/selenium/test_exercises_management.robot

# Run tests with specific tag
robot -i smoke tests/selenium/
```

### Test Tags
- `smoke` - Critical path tests
- `access-control` - Access verification tests
- `crud` - Create/Read/Update/Delete operations
- `role-<rolename>` - Tests for specific roles
- `slow` - Long-running tests to skip in CI

---

## Expected Timeline

| Phase | Files | Estimated Tests | Timeline |
|-------|-------|---|---|
| Phase 1 (Complete) | 3 | 6 | ✅ Done |
| Phase 2 | 3 | 18 | Week 1-2 |
| Phase 3 | 2 | 12 | Week 2-3 |
| Phase 4 | 1 | 15 | Week 3 |
| Phase 5 | 2 | 10 | Week 4 |
| **Total** | **11** | **61** | **~4 weeks** |

---

## Notes & Considerations

1. **Date Input Handling**: HTML5 date inputs require JavaScript automation
2. **Alert Handling**: Exercise deletion uses confirmation dialogs
3. **Flash Messages**: Verify success/error messages for all operations
4. **Pagination**: Consider pagination if many items (exercises, starters)
5. **Sorting**: Verify results sorting by points
6. **Cascading Deletes**: Ensure data consistency after deletions
7. **Concurrency**: Test with multiple users entering points simultaneously (if applicable)
8. **Performance**: Monitor page load times, especially for large result sets

---

## Success Criteria

- [ ] All 61 test cases defined
- [ ] 100% page coverage in pages.md
- [ ] Access control matrix fully tested
- [ ] All CRUD operations verified
- [ ] All role-based features validated
- [ ] Error handling tested
- [ ] Edge cases documented and tested
- [ ] Tests run successfully in CI/CD pipeline
- [ ] >95% pass rate maintained

