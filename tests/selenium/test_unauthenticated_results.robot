*** Settings ***
Library           SeleniumLibrary
Documentation     Test suite for access control on the exercise results page
...               (http://localhost:5000/exercises/results/<id>).
...               Covers: unauthenticated users see "No results available yet" and no
...               management buttons; authenticated admin sees "Publish Results" button.
...
...               Suite requirements:
...               - Flask web app running at http://localhost:5000 (started by __init__.robot suite setup)
...               - A competition with ID=1 must exist — run test_user_login.robot first
...               - Admin user (username: admin, password: admin) in the database
...               - Chrome/Chromium and ChromeDriver installed for headlesschrome

*** Variables ***
${INDEX_PAGE}         http://localhost:5000/
${LOGIN_PAGE}         http://localhost:5000/users/login
${BROWSER}            headlesschrome

*** Test Cases ***
Test Unauthenticated User Can View Unpublished Results Page
    [Documentation]    Verifies that an unauthenticated visitor can access the results page
    ...    for competition ID=1 and sees "No results available yet" with the sub-message
    ...    "Points need to be entered for exercises". Also verifies that the
    ...    "Publish Results" and "Unpublish Results" management buttons are NOT shown.
    ...
    ...    Requirements: Flask app running; competition ID=1 exists (created by test_user_login.robot);
    ...    Chrome/ChromeDriver installed.
    [Tags]    results    unauthenticated    access-control
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    
    # Navigate directly to results page without being logged in
    # The first competition created by test_user_login.robot has ID 1
    Go To    http://localhost:5000/exercises/results/1
    
    # Should see the results page with "No results available yet" message
    Wait Until Page Contains    No results available yet    timeout=15s
    Page Should Contain    Points need to be entered for exercises
    
    # Verify that publish/unpublish buttons are NOT visible for unauthenticated user
    Page Should Not Contain    Publish Results
    Page Should Not Contain    Unpublish Results
    
    Close Browser

Test Authenticated Admin Can Manage Results
    [Documentation]    Verifies that an authenticated admin user can access the results page
    ...    for competition ID=1 and sees the "Publish Results" management button in addition
    ...    to the "No results available yet" message.
    ...
    ...    Requirements: Flask app running; competition ID=1 exists (created by test_user_login.robot);
    ...    admin user (admin/admin) exists; Chrome/ChromeDriver installed.
    [Tags]    results    authenticated    access-control    admin
    # Login as admin
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    Input Text    name:username    admin
    Input Text    name:password    admin
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Workingtest Planer    timeout=10s
    
    # Navigate to results page for the first competition
    Go To    http://localhost:5000/exercises/results/1
    
    # Should see the results page with "No results available yet" message
    Wait Until Page Contains    No results available yet    timeout=15s
    
    # Verify that publish/unpublish buttons ARE visible for admin
    Page Should Contain    Publish Results
    
    Close Browser
