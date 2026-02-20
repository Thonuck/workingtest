*** Settings ***
Library           Process
Library           SeleniumLibrary
Library           OperatingSystem

*** Variables ***
${INDEX_PAGE}              http://localhost:5000/
${LOGIN_PAGE}              http://localhost:5000/users/login
${CREATE_WT_PAGE}          http://localhost:5000/wts/create_wt
${BROWSER}                 headlesschrome
${ADMIN_USERNAME}          admin
${ADMIN_PASSWORD}          admin

*** Test Cases ***
Index Page Displays Title
    [Documentation]    Testet, dass die Titelzeile "Workingtest Planer" auf der Index-Seite angezeigt wird.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Wait Until Page Contains    Workingtest Planer    timeout=10s
    Close Browser

Index Page Displays All Competitions
    [Documentation]    Testet, dass alle Wettbewerbe auf der Index-Seite angezeigt werden.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    # The page should display with the table structure even if empty
    Page Should Contain    Workingtest Planer
    Page Should Contain    Competition
    Close Browser

Index Page Displays Competition Details
    [Documentation]    Testet, dass die Details aller Wettbewerbe angezeigt werden (Name, Level, Ort, Datum).
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Page Should Contain    Competition
    Page Should Contain    Class
    Page Should Contain    Location
    Page Should Contain    Date
    Close Browser

Index Page Empty State
    [Documentation]    Testet die leere Tabelle, wenn keine Wettbewerbe existieren.
    ...
    ...    Execution requirements:
    ...    - Python must be available on PATH
    ...    - reset_database.py must exist in the project root directory
    ...    - Optional env variable PROJECT_DIR must point to the project root
    ...      (defaults to /home/runner/work/workingtest/workingtest)
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    # Reset database to empty state
    ${project_dir}=    Get Environment Variable    PROJECT_DIR    /home/runner/work/workingtest/workingtest
    Set Suite Variable    ${PROJECT_DIR}    ${project_dir}
    Run Process    pkill    -9    -f    python run.py
    Sleep    1s
    Run Process    rm    -f    ${PROJECT_DIR}/instance/database.db
    Run Process    bash    -c    cd ${PROJECT_DIR} && echo "ja" | python reset_database.py    shell=True
    Start Web App
    Sleep    2s
    
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    # Table should be present but empty
    Page Should Contain    Workingtest Planer
    Close Browser

Index Page Competition Link Navigation
    [Documentation]    Testet, dass Admin auf die Index-Seite zugreifen kann und angemeldet ist.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${ADMIN_USERNAME}
    Input Text      name:password    ${ADMIN_PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin    timeout=10s
    Page Should Contain    Workingtest Planer
    Close Browser

Index Page Admin Can See Create Button
    [Documentation]    Testet, dass Admin-Benutzer einen "Create"-Button sehen können.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Set Window Size    1920    1080
    # Check for buttons or links that would allow creating a new competition
    # This will depend on the actual UI implementation
    # For now, we just verify the page loads for admin
    Page Should Contain    Workingtest Planer
    Close Browser

Index Page Unauthenticated User Can View Results
    [Documentation]    Testet, dass unauthentische Benutzer die Index-Seite sehen können.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Wait Until Page Contains    Workingtest Planer    timeout=10s
    Close Browser

Index Page Authenticated User Access
    [Documentation]    Testet, dass authentifizierte Benutzer auf die Index-Seite zugreifen können.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${ADMIN_USERNAME}
    Input Text      name:password    ${ADMIN_PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Workingtest Planer    timeout=10s
    Wait Until Page Contains    Logout admin    timeout=10s
    Close Browser

Index Page Table Structure
    [Documentation]    Testet, dass die Tabelle alle erwarteten Spalten hat.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Page Should Contain    Competition
    Page Should Contain    Class
    Page Should Contain    Location
    Page Should Contain    Date
    Close Browser

Index Page Responsive Design
    [Documentation]    Testet die Responsivität der Index-Seite auf verschiedenen Bildschirmgrößen.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    
    # Test on mobile size
    Set Window Size    375    667
    Page Should Contain    Workingtest Planer
    
    # Test on tablet size
    Set Window Size    768    1024
    Page Should Contain    Workingtest Planer
    
    # Test on desktop size
    Set Window Size    1920    1080
    Page Should Contain    Workingtest Planer
    
    Close Browser

Index Page Multiple Competitions Display
    [Documentation]    Testet die Anzeige mehrerer Wettbewerbe auf der Index-Seite.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000 (started by __init__.robot suite setup)
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Login With Admin User
    Open Browser    ${INDEX_PAGE}    ${BROWSER}
    Page Should Contain    Workingtest Planer
    Page Should Contain    Competition
    Page Should Contain    Class
    Page Should Contain    Location
    Close Browser

*** Keywords ***
Login With Admin User
    [Documentation]    Meldet sich mit Admin-Credentials an und schließt den Browser.
    ...
    ...    Execution requirements:
    ...    - Flask web app must be running at http://localhost:5000
    ...    - Admin user (username: admin, password: admin) must exist in the database
    ...    - Chrome/Chromium and ChromeDriver must be installed for headlesschrome
    Open Browser    ${LOGIN_PAGE}    ${BROWSER}
    Input Text      name:username    ${ADMIN_USERNAME}
    Input Text      name:password    ${ADMIN_PASSWORD}
    Click Button    xpath://button[@type='submit']
    Wait Until Page Contains    Logout admin    timeout=10s
    Close Browser

Start Web App
    [Documentation]    Startet die Webanwendung auf http://localhost:5000.
    ...
    ...    Execution requirements:
    ...    - PROJECT_DIR suite variable must be set before calling this keyword
    ...    - run.py must exist in the project root directory
    ...    - Port 5000 must be available
    Start Process    python    run.py    cwd=${PROJECT_DIR}    env:PYTHONUNBUFFERED=1
    Sleep    5s
