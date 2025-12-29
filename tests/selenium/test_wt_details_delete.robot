*** Settings ***
Library           Process
Library           SeleniumLibrary
Suite Setup       Start Web App
Suite Teardown    Stop Web App

*** Variables ***
${LOGIN_PAGE}         http://localhost:5000/users/login
${INDEX_PAGE}         http://localhost:5000/
${BROWSER}            headlesschrome
${USERNAME}           admin
${PASSWORD}           admin
${WT_NAME}            Test WT Details
${WT_LEVEL}           A
${WT_LOCATION}        Test Location
${WT_DATE}            15.01.2025

*** Test Cases ***
Test WT Details And Delete
    [Documentation]    Testet das Anlegen eines WT, Anzeigen der Details und Löschen.
    # 1. Login und neuen WT anlegen
    Login With Admin User
    Click Link    WT erstellen
    Input Text    name:name        ${WT_NAME}
    Select From List By Value    name:level    ${WT_LEVEL}
    Input Text    name:location    ${WT_LOCATION}
    Input Text    name:date        ${WT_DATE}
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
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    Input Text      name:username    ${USERNAME}
    Input Text      name:password    ${PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin    timeout=10s

Start Web App
    [Documentation]    Startet die Webanwendung.
    Start Process     python    run.py
    Sleep    5s

Stop Web App
    [Documentation]    Stoppt die Webanwendung.
    Terminate All Processes
