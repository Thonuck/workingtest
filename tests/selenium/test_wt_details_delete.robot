*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${LOGIN_PAGE}         http://localhost:5000/users/login
${INDEX_PAGE}         http://localhost:5000/
${BROWSER}            headlesschrome
${USERNAME}           admin
${PASSWORD}           admin
${WT_NAME}            Test WT Details
${WT_LEVEL}           A
${WT_LOCATION}        Test Location
${WT_DATE}            2025-01-15

*** Test Cases ***
Test WT Details And Delete
    [Documentation]    Testet das Anlegen eines WT, Anzeigen der Details und Löschen.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    ...    - A link to /wts/create_wt must be visible on the index page for admin users
    # 1. Login und neuen WT anlegen
    Login With Admin User
    Click Link    xpath://a[@href='/wts/create_wt']
    Input Text    name:name        ${WT_NAME}
    Select From List By Value    name:level    ${WT_LEVEL}
    Input Text    name:location    ${WT_LOCATION}
    Execute JavaScript    document.querySelector('input[name="date"]').value = '${WT_DATE}'
    Click Button  xpath://button[@type='submit']
    Wait Until Page Contains    ${WT_NAME}    timeout=15s
    
    # 2. Detail Seite aufrufen
    Click Element    xpath://td[contains(text(), '${WT_NAME}')]/ancestor::tr
    Wait Until Page Contains    Workingtest Details    timeout=10s
    Page Should Contain    ${WT_NAME}
    Page Should Contain    ${WT_LEVEL}
    Page Should Contain    ${WT_LOCATION}
    
    # 3. WT löschen
    Click Button    xpath://button[contains(text(), 'Löschen')]
    Handle Alert    action=ACCEPT
    Wait Until Location Is    ${INDEX_PAGE}    timeout=10s
    
    # 4. Überprüfen, ob gelöscht wurde
    Page Should Not Contain    ${WT_NAME}
    Close Browser

*** Keywords ***
Login With Admin User
    [Documentation]    Öffnet den Browser, meldet sich mit Admin-Credentials an und hält die Session offen.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    Input Text      name:username    ${USERNAME}
    Input Text      name:password    ${PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin    timeout=10s
