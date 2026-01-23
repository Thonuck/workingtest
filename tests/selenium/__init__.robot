*** Settings ***
Library           Process
Library           OperatingSystem
Suite Setup       Reset Database And Start Web App
Suite Teardown    Stop Web App

*** Keywords ***
Reset Database And Start Web App
    [Documentation]    Setzt die Datenbank zurück und startet die Webanwendung für alle Tests.
    Run Process    pkill    -9    -f    python run.py
    Sleep    1s
    Run Process    rm    -f    /home/thomas/development/workingtest/instance/database.db
    ${result}=    Run Process    bash    -c    cd /home/thomas/development/workingtest && source .venv/bin/activate && echo "ja" | python reset_database.py    shell=True
    Start Web App

Start Web App
    [Documentation]    Startet die Webanwendung.
    Start Process    python    run.py    cwd=/home/thomas/development/workingtest    env:PYTHONUNBUFFERED=1
    Sleep    5s

Stop Web App
    [Documentation]    Stoppt die Webanwendung.
    Terminate All Processes
