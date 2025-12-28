*** Settings ***
Library           Process
Library           SeleniumLibrary
Suite Setup       Start Web App
Suite Teardown    Stop Web App

*** Variables ***
${LOGIN_PAGE}         http://localhost:5000/users/login
${BROWSER}     headlesschrome
${USERNAME}    admin
${PASSWORD}    admin

*** Test Cases ***
Test User Login
    [Documentation]    Testet den Login eines Benutzers.
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${USERNAME}
    Input Text      name:password    ${PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin
    Close Browser

Test Create Competition
    [Documentation]    Testet die Erstellung eines neuen Wettbewerbs.
    Competition Should not exist    Test Wettbewerb
    Create Competition    name=Test Wettbewerb    level=A    location=Testort    date=01.12.2024
    Open Browser    http://localhost:5000/    ${BROWSER}
    Wait Until Page Contains    Test Wettbewerb
    Close Browser

*** Keywords ***
Login With Admin User
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${USERNAME}
    Input Text      name:password    ${PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin

Competition Should not exist
    [Arguments]    ${name}
    [Documentation]    Überprüft, dass kein Wettbewerb mit dem angegebenen Namen und Level existiert.
    Open Browser    http://localhost:5000/    ${BROWSER}
    Set Window Size    1920    1080
    Page Should Not Contain    ${name}
    Close Browser

Create Competition
    [Arguments]    ${name}    ${level}    ${location}    ${date}
    [Documentation]    Erstellt einen neuen Wettbewerb mit den angegebenen Details.
    Login With Admin User
    Click Link    xpath://a[@href='/wts/create_wt']
    Input Text    name:name        ${name}
    Select From List By Value    name:level    ${level}
    Input Text    name:location    ${location}
    Input Text    name:date        ${date}
    Click Button  xpath://button[@type='submit']
    Wait Until Page Contains    ${name}
    Close Browser

Start Web App
    [Documentation]    Startet die Webanwendung.
    Start Process     python    run.py
    Sleep    5s

Stop Web App
    [Documentation]    Stoppt die Webanwendung.
    Terminate All Processes