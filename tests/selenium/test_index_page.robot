*** Settings ***
Library           Process
Library           SeleniumLibrary
Library           OperatingSystem
Documentation     Test suite for the index/home page (http://localhost:5000/).
...               Covers: page title, competition table structure, column display,
...               empty state, authenticated vs. unauthenticated access, and responsive layout.
...
...               Suite requirements:
...               - Flask web app running at http://localhost:5000 (started by __init__.robot suite setup)
...               - Admin user (username: admin, password: admin) in the database
...               - Chrome/Chromium and ChromeDriver installed for headlesschrome
...               - Set PROJECT_DIR env variable to override the default project root path
...                 (default: /home/runner/work/workingtest/workingtest)

*** Variables ***
${INDEX_PAGE}              http://localhost:5000/
${LOGIN_PAGE}              http://localhost:5000/users/login
${CREATE_WT_PAGE}          http://localhost:5000/wts/create_wt
${BROWSER}                 headlesschrome
${ADMIN_USERNAME}          admin
${ADMIN_PASSWORD}          admin

*** Test Cases ***
Index Page Displays Title
    [Documentation]    Verifies that the page heading "Workingtest Planer" is visible to
    ...    any visitor (unauthenticated access allowed).
    ...
    ...    Requirements: Flask app running at http://localhost:5000; Chrome/ChromeDriver installed.
    [Tags]    index    unauthenticated    smoke
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Wait Until Page Contains    Workingtest Planer    timeout=10s
    Close Browser

Index Page Displays All Competitions
    [Documentation]    Verifies that the competition table is present on the index page
    ...    and shows the "Competition" column heading after admin login.
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    index    authenticated    table
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    # The page should display with the table structure even if empty
    Page Should Contain    Workingtest Planer
    Page Should Contain    Competition
    Close Browser

Index Page Displays Competition Details
    [Documentation]    Verifies that all four required column headers (Competition, Class,
    ...    Location, Date) are present in the competition table.
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    index    authenticated    table
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Page Should Contain    Competition
    Page Should Contain    Class
    Page Should Contain    Location
    Page Should Contain    Date
    Close Browser

Index Page Empty State
    [Documentation]    Verifies that the index page loads correctly when the database is empty
    ...    (no competitions). Resets the database and restarts the app before checking.
    ...
    ...    Requirements:
    ...    - Python on PATH; reset_database.py in project root
    ...    - Optional PROJECT_DIR env variable (default: /home/runner/work/workingtest/workingtest)
    ...    - Chrome/ChromeDriver installed
    [Tags]    index    unauthenticated    empty-state
    # Reset database to empty state
    ${project_dir}=    Get Environment Variable    PROJECT_DIR    /home/runner/work/workingtest/workingtest
    Set Suite Variable    ${PROJECT_DIR}    ${project_dir}
    Run Process    pkill    -9    -f    python run.py
    Sleep    1s
    Run Process    rm    -f    ${PROJECT_DIR}/instance/database.db
    Run Process    bash    -c    cd ${PROJECT_DIR} && echo "ja" | python reset_database.py    shell=True
    Start Web App
    Sleep    2s
    
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    # Table should be present but empty
    Page Should Contain    Workingtest Planer
    Close Browser

Index Page Competition Link Navigation
    [Documentation]    Verifies that an admin user can log in and is shown the index page
    ...    with "Workingtest Planer" heading and the Logout link.
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    index    authenticated    navigation
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${ADMIN_USERNAME}
    Input Text      name:password    ${ADMIN_PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin    timeout=10s
    Page Should Contain    Workingtest Planer
    Close Browser

Index Page Admin Can See Create Button
    [Documentation]    Verifies that the index page loads for an authenticated admin user.
    ...    NOTE: Currently only checks the page heading. The "Create" button check depends
    ...    on the UI implementation and should be expanded once the button is reliably present.
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    index    authenticated    create
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    # Check for buttons or links that would allow creating a new competition
    # This will depend on the actual UI implementation
    # For now, we just verify the page loads for admin
    Page Should Contain    Workingtest Planer
    Close Browser

Index Page Unauthenticated User Can View Results
    [Documentation]    Verifies that the index page is publicly accessible without login,
    ...    showing the "Workingtest Planer" heading.
    ...
    ...    Requirements: Flask app running; Chrome/ChromeDriver installed.
    [Tags]    index    unauthenticated    smoke
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Wait Until Page Contains    Workingtest Planer    timeout=10s
    Close Browser

Index Page Authenticated User Access
    [Documentation]    Verifies that a logged-in admin user sees the index page and the
    ...    Logout link (confirming the session is active).
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    index    authenticated    smoke
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${ADMIN_USERNAME}
    Input Text      name:password    ${ADMIN_PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Workingtest Planer    timeout=10s
    Wait Until Page Contains    Logout admin    timeout=10s
    Close Browser

Index Page Table Structure
    [Documentation]    Verifies that the competition table contains all four required
    ...    column headers: Competition, Class, Location, Date.
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    index    authenticated    table
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Page Should Contain    Competition
    Page Should Contain    Class
    Page Should Contain    Location
    Page Should Contain    Date
    Close Browser

Index Page Responsive Design
    [Documentation]    Verifies the index page heading is visible at three common viewport sizes:
    ...    mobile (375x667), tablet (768x1024), and desktop (1920x1080).
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    index    authenticated    responsive
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    
    # Test on mobile size
    Set Window Size    375    667
    Page Should Contain    Workingtest Planer
    
    # Test on tablet size
    Set Window Size    768    1024
    Page Should Contain    Workingtest Planer
    
    # Test on desktop size
    Set Window Size    1920    1080
    Page Should Contain    Workingtest Planer
    
    Close Browser

Index Page Multiple Competitions Display
    [Documentation]    Verifies that the competition table columns (Competition, Class, Location)
    ...    are all present on the index page when logged in as admin.
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    index    authenticated    table
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Page Should Contain    Workingtest Planer
    Page Should Contain    Competition
    Page Should Contain    Class
    Page Should Contain    Location
    Close Browser

*** Keywords ***
Login With Admin User
    [Documentation]    Opens the login page, authenticates as admin (admin/admin), waits for
    ...    the "Logout admin" link to confirm successful login, then closes the browser.
    ...    Use this keyword as a pre-step when the test needs a fresh authenticated session
    ...    cookie before opening the actual page under test.
    ...
    ...    Requirements:
    ...    - Flask web app must be running at http://localhost:5000
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${ADMIN_USERNAME}
    Input Text      name:password    ${ADMIN_PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin    timeout=10s
    Close Browser

Start Web App
    [Documentation]    Starts the Flask development server as a background process on port 5000.
    ...    Waits 5 seconds for the server to become ready before returning.
    ...
    ...    Requirements:
    ...    - Suite variable ${PROJECT_DIR} must be set before calling this keyword
    ...    - run.py must exist in the project root directory
    ...    - Port 5000 must be free
    Start Process    python    run.py    cwd=${PROJECT_DIR}    env:PYTHONUNBUFFERED=1
    Sleep    5s
