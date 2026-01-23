*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${INDEX_PAGE}         http://localhost:5000/
${LOGIN_PAGE}         http://localhost:5000/users/login
${BROWSER}            headlesschrome

*** Test Cases ***
Test Unauthenticated User Can View Unpublished Results Page
    [Documentation]    Testet, dass nicht eingeloggte Benutzer die Results-Seite sehen können und "No results available yet" angezeigt wird, wenn keine Daten vorhanden sind.
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
    [Documentation]    Testet, dass ein Admin-Benutzer die Results-Seite mit Publish/Unpublish-Buttons sehen kann.
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
