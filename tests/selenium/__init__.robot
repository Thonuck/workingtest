*** Settings ***
Library           Process
Library           OperatingSystem
Suite Setup       Reset Database And Start Web App
Suite Teardown    Stop Web App

*** Keywords ***
Reset Database And Start Web App
    [Documentation]    Setzt die Datenbank zurück und startet die Webanwendung für alle Tests.
    ${project_dir}=    Get Environment Variable    PROJECT_DIR    /home/runner/work/workingtest/workingtest
    Set Suite Variable    ${PROJECT_DIR}    ${project_dir}
    Run Process    pkill    -9    -f    python run.py
    Sleep    1s
    Run Process    rm    -f    ${PROJECT_DIR}/instance/database.db
    ${result}=    Run Process    bash    -c    cd ${PROJECT_DIR} && echo "ja" | python reset_database.py    shell=True
    Start Web App

Start Web App
    [Documentation]    Startet die Webanwendung.
    Start Process    python    run.py    cwd=${PROJECT_DIR}    env:PYTHONUNBUFFERED=1
    Sleep    5s

Stop Web App
    [Documentation]    Stoppt die Webanwendung.
    Terminate All Processes
