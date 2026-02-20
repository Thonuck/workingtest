*** Settings ***
Library           Process
Library           OperatingSystem
Suite Setup       Reset Database And Start Web App
Suite Teardown    Stop Web App

*** Keywords ***
Reset Database And Start Web App
    [Documentation]    Setzt die Datenbank zurück und startet die Webanwendung für alle Tests.
    ...
    ...    Execution requirements:
    ...    - Python must be available on PATH
    ...    - reset_database.py must exist in the project root directory
    ...    - Optional env variable PROJECT_DIR must point to the project root
    ...      (defaults to /home/runner/work/workingtest/workingtest)
    ...    - The reset script creates an admin user (username: admin, password: admin)
    ${project_dir}=    Get Environment Variable    PROJECT_DIR    /home/runner/work/workingtest/workingtest
    Set Suite Variable    ${PROJECT_DIR}    ${project_dir}
    Run Process    pkill    -9    -f    python run.py
    Sleep    1s
    Run Process    rm    -f    ${PROJECT_DIR}/instance/database.db
    ${result}=    Run Process    bash    -c    cd ${PROJECT_DIR} && echo "ja" | python reset_database.py    shell=True
    Start Web App

Start Web App
    [Documentation]    Startet die Webanwendung auf http://localhost:5000.
    ...
    ...    Execution requirements:
    ...    - PROJECT_DIR suite variable must be set (done by Reset Database And Start Web App)
    ...    - run.py must exist in the project root directory
    ...    - Port 5000 must be available
    Start Process    python    run.py    cwd=${PROJECT_DIR}    env:PYTHONUNBUFFERED=1
    Sleep    5s

Stop Web App
    [Documentation]    Stoppt alle gestarteten Prozesse, einschließlich der Webanwendung.
    ...
    ...    Execution requirements:
    ...    - Must be called after Start Web App to properly clean up processes
    Terminate All Processes
