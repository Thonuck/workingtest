*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${BROWSER}            headlesschrome

*** Test Cases ***
Test Debug Results Page Content
    [Documentation]    Debug test to see what's actually on the results page.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - A competition with ID=1 must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    http://localhost:5000/exercises/results/1    ${BROWSER}
    Set Window Size    1920    1080
    
    # Get the page source and save it
    ${page_source}=    Get Page Source
    Log    ${page_source}
    
    # Check what text is visible
    ${visible_text}=    Get Text    xpath://body
    Log    Visible text: ${visible_text}
    
    Close Browser
