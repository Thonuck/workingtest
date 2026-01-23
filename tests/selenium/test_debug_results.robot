*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${BROWSER}            headlesschrome

*** Test Cases ***
Test Debug Results Page Content
    [Documentation]    Debug test to see what's actually on the results page.
    Open Browser    http://localhost:5000/exercises/results/1    ${BROWSER}
    Set Window Size    1920    1080
    
    # Get the page source and save it
    ${page_source}=    Get Page Source
    Log    ${page_source}
    
    # Check what text is visible
    ${visible_text}=    Get Text    xpath://body
    Log    Visible text: ${visible_text}
    
    Close Browser
