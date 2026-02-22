*** Settings ***
Library           SeleniumLibrary
Documentation     Test suite for the User Management pages.
...               Covers: user detail view, user edit form, register (new user) form.
...               All tests run as admin unless noted otherwise.
...
...               Requirements:
...               - Flask web app running at http://localhost:5000 (started by __init__.robot)
...               - Admin user (username: admin, password: admin) in the database
...               - Chrome/Chromium and ChromeDriver installed

*** Variables ***
${BASE_URL}       http://localhost:5000
${LOGIN_PAGE}     http://localhost:5000/users/login
${USERS_PAGE}     http://localhost:5000/users/
${REGISTER_PAGE}  http://localhost:5000/users/register
${BROWSER}        headlesschrome
${ADMIN_USER}     admin
${ADMIN_PASS}     admin

*** Test Cases ***

Register Page Displays Form
    [Documentation]    Verifies the register page shows the "Neuen Benutzer registrieren"
    ...    heading and input fields for username and password.
    [Tags]    register    form    unauthenticated
    Open Browser    ${REGISTER_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    Wait Until Page Contains    Neuen Benutzer registrieren
    Page Should Contain Element    name:username
    Page Should Contain Element    name:password
    Page Should Contain Button    xpath://button[@type='submit']
    Close Browser

Register New User Via Form
    [Documentation]    Verifies that submitting the registration form creates a new user
    ...    and redirects to the login page.
    [Tags]    register    create    unauthenticated
    Open Browser    ${REGISTER_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    Wait Until Page Contains    Neuen Benutzer registrieren
    Input Text      name:username    selenium_test_user
    Input Text      name:password    TestPassword123
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Login
    Close Browser

User Detail Page Displays Fields
    [Documentation]    Verifies the user detail page for admin shows ID, Benutzername,
    ...    Rolle and action buttons (Edit, Delete, Back) rendered by generic_details.
    [Tags]    detail    authenticated    generic_details
    Login As Admin
    Go To    ${USERS_PAGE}
    Wait Until Page Contains    Users
    ${detail_url}=    Get Element Attribute    xpath://a[contains(@href,'/detail')]    href
    Go To    ${BASE_URL}${detail_url}
    Wait Until Page Contains    admin
    Page Should Contain    ID
    Page Should Contain    Benutzername
    Page Should Contain    Rolle
    Page Should Contain    Edit
    Page Should Contain    Delete
    Page Should Contain    Back
    Close Browser

User Edit Page Displays Form
    [Documentation]    Verifies the user edit page shows "Benutzer bearbeiten" heading,
    ...    username input, role select, password input, and action buttons via generic_details.
    [Tags]    edit    authenticated    generic_details
    Login As Admin
    Go To    ${USERS_PAGE}
    Wait Until Page Contains    Users
    ${edit_url}=    Get Element Attribute    xpath://a[contains(@href,'/edit')]    href
    Go To    ${BASE_URL}${edit_url}
    Wait Until Page Contains    Benutzer bearbeiten
    Page Should Contain Element    name:username
    Page Should Contain Element    name:role
    Page Should Contain Element    name:password
    Page Should Contain Button    xpath://button[@type='submit']
    Page Should Contain    Speichern
    Page Should Contain    Abbrechen
    Close Browser

*** Keywords ***

Login As Admin
    [Documentation]    Opens the login page, authenticates as admin, and waits for the
    ...    "Logout admin" link confirming a successful login.
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    Input Text      name:username    ${ADMIN_USER}
    Input Text      name:password    ${ADMIN_PASS}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin
