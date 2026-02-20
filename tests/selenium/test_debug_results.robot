*** Settings ***
Library           SeleniumLibrary
Documentation     Debug helper suite for inspecting the raw content of the exercise results page.
...               Logs the full page source and visible body text so that test authors can
...               determine the exact element names/text for writing proper assertions.
...
...               NOTE: This is not a functional test. It does not assert any specific content.
...               Run it manually when the results page content is unknown or has changed.
...
...               Suite requirements:
...               - Flask web app running at http://localhost:5000 (started by __init__.robot suite setup)
...               - A competition with ID=1 must exist in the database
...               - Chrome/Chromium and ChromeDriver installed for headlesschrome

*** Variables ***
${BROWSER}            headlesschrome

*** Test Cases ***
Test Debug Results Page Content
    [Documentation]    Navigates to the results page for competition ID=1, logs the full
    ...    HTML page source and the visible body text to the Robot Framework report.
    ...    No assertions are made — this test always passes if the page loads.
    ...    Use the logged output to determine correct selectors and text for real assertions.
    ...
    ...    Requirements: Flask app running; competition ID=1 exists; Chrome/ChromeDriver installed.
    [Tags]    debug    results    manual
    Open Browser    http://localhost:5000/exercises/results/1    ${BROWSER}
    Set Window Size    1920    1080
    
    # Get the page source and save it
    ${page_source}=    Get Page Source
    Log    ${page_source}
    
    # Check what text is visible
    ${visible_text}=    Get Text    xpath://body
    Log    Visible text: ${visible_text}
    
    Close Browser
