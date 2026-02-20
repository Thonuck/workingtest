*** Settings ***
Library           Process
Library           SeleniumLibrary
Library           OperatingSystem
Documentation     Test suite for user authentication and competition creation.
...               Covers: admin login flow and creating a new Workingtest competition
...               via the web UI.
...
...               NOTE: This suite must run BEFORE test_unauthenticated_results.robot and
...               test_debug_results.robot because it creates the competition with ID=1
...               that those suites depend on.
...
...               Suite requirements:
...               - Flask web app running at http://localhost:5000 (started by __init__.robot suite setup)
...               - Admin user (username: admin, password: admin) in the database
...               - Chrome/Chromium and ChromeDriver installed for headlesschrome

*** Variables ***
${LOGIN_PAGE}         http://localhost:5000/users/login
${BROWSER}     headlesschrome
${USERNAME}    admin
${PASSWORD}    admin

*** Test Cases ***
Test User Login
    [Documentation]    Verifies that the admin user can log in successfully and that
    ...    the "Logout admin" link appears after authentication.
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    login    authentication    smoke
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${USERNAME}
    Input Text      name:password    ${PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin
    Close Browser

Test Create Competition
    [Documentation]    Verifies that an admin user can create a new Workingtest competition
    ...    and that it subsequently appears on the index page.
    ...    Creates "Test Wettbewerb" (level A, location Testort, date 2024-12-01).
    ...
    ...    Requirements: Flask app running; admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    ...    NOTE: Depends on a clean database where "Test Wettbewerb" does not yet exist.
    [Tags]    competition    create    authenticated
    Competition Should not exist    Test Wettbewerb
    Create Competition    name=Test Wettbewerb    level=A    location=Testort    date=2024-12-01
    Open Browser    http://localhost:5000/    ${BROWSER}
    Wait Until Page Contains    Test Wettbewerb    timeout=15s
    Close Browser

*** Keywords ***
Login With Admin User
    [Documentation]    Opens the login page, authenticates as admin (admin/admin), waits for
    ...    the "Logout admin" link confirming a successful login, and keeps the browser open
    ...    so subsequent steps in the same test can navigate further.
    ...
    ...    Requirements:
    ...    - Flask web app must be running at http://localhost:5000
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${USERNAME}
    Input Text      name:password    ${PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin

Competition Should not exist
    [Arguments]    ${name}
    [Documentation]    Verifies that no competition with the given name is shown on the
    ...    index page. Opens a new browser window, checks the index page, then closes it.
    ...
    ...    Arguments:
    ...    - name: The competition name that must NOT appear on the index page
    ...
    ...    Requirements:
    ...    - Flask web app must be running at http://localhost:5000
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    http://localhost:5000/    ${BROWSER}
    Set Window Size    1920    1080
    Page Should Not Contain    ${name}
    Close Browser

Create Competition
    [Arguments]    ${name}    ${level}    ${location}    ${date}
    [Documentation]    Logs in as admin, navigates to the create competition form, fills in
    ...    all fields, submits, and waits for a redirect back to the index page.
    ...
    ...    Arguments:
    ...    - name: Competition name (text input)
    ...    - level: Competition level, e.g. A, F, or O (select list value)
    ...    - location: Competition location (text input)
    ...    - date: Competition date in YYYY-MM-DD format (set via JavaScript)
    ...
    ...    Requirements:
    ...    - Flask web app must be running at http://localhost:5000
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Login With Admin User
    Click Link    xpath://a[@href='/wts/create_wt']
    Input Text    name:name        ${name}
    Select From List By Value    name:level    ${level}
    Input Text    name:location    ${location}
    Execute JavaScript    document.querySelector('input[name="date"]').value = '${date}'
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Workingtest Planer    timeout=10s
    Close Browser