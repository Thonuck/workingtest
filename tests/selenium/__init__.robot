*** Settings ***
Library           Process
Library           OperatingSystem
Suite Setup       Reset Database And Start Web App
Suite Teardown    Stop Web App
Documentation     Shared suite setup and teardown keywords for all selenium tests.
...               This resource file is automatically loaded by Robot Framework for any
...               test suite under the tests/selenium/ directory.
...
...               Suite execution order:
...               1. test_user_login.robot - verifies admin login and creates the first competition (ID=1)
...               2. test_index_page.robot - tests the index/home page
...               3. test_wt_details_delete.robot - tests WT detail view and deletion
...               4. test_unauthenticated_results.robot - tests results page access control
...               5. test_debug_results.robot - debug helper for the results page
...
...               NOTE: The admin user (admin/admin) is created by reset_database.py during
...               suite setup, not by test_user_login.robot.
...
...               Global execution requirements:
...               - Python 3.8+ on PATH
...               - Chrome/Chromium and matching ChromeDriver installed
...               - Port 5000 available for the Flask dev server
...               - Set PROJECT_DIR env variable to the project root if not running from
...                 /home/runner/work/workingtest/workingtest

*** Keywords ***
Reset Database And Start Web App
    [Documentation]    Resets the database and starts the Flask web app on http://localhost:5000.
    ...    Called automatically as Suite Setup before any test in the selenium suite runs.
    ...
    ...    Steps performed:
    ...    1. Reads PROJECT_DIR from the environment (default: /home/runner/work/workingtest/workingtest)
    ...    2. Kills any running Flask process to avoid port conflicts
    ...    3. Deletes the existing SQLite database file
    ...    4. Runs reset_database.py to create a fresh schema with seed data including
    ...       an admin user (username: admin, password: admin)
    ...    5. Starts the Flask dev server as a background process
    ...
    ...    Requirements:
    ...    - Python must be available on PATH
    ...    - reset_database.py must exist in the project root directory
    ...    - Optional env variable PROJECT_DIR must point to the project root
    ...      (defaults to /home/runner/work/workingtest/workingtest)
    ${project_dir}=    Get Environment Variable    PROJECT_DIR    /home/runner/work/workingtest/workingtest
    Set Suite Variable    ${PROJECT_DIR}    ${project_dir}
    Run Process    pkill    -9    -f    python run.py
    Sleep    1s
    Run Process    rm    -f    ${PROJECT_DIR}/instance/database.db
    ${result}=    Run Process    bash    -c    cd ${PROJECT_DIR} && echo "ja" | python reset_database.py    shell=True
    Start Web App

Start Web App
    [Documentation]    Starts the Flask development server as a background process on port 5000.
    ...    Waits 5 seconds for the server to become ready before returning.
    ...
    ...    Requirements:
    ...    - Suite variable ${PROJECT_DIR} must be set (set by Reset Database And Start Web App)
    ...    - run.py must exist in the project root directory
    ...    - Port 5000 must be free
    Start Process    python    run.py    cwd=${PROJECT_DIR}    env:PYTHONUNBUFFERED=1
    Sleep    5s

Stop Web App
    [Documentation]    Terminates all background processes started during the suite, including the Flask server.
    ...    Called automatically as Suite Teardown after all tests in the selenium suite finish.
    ...
    ...    Requirements:
    ...    - Must be called after Start Web App to properly clean up processes
    Terminate All Processes
