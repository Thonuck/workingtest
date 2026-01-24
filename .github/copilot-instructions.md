**Running Robot**

Always run robot with -L TRACE and use outut.xml for further analysis.
don't use timeouts when running robotframework.
Use always the existing virtual environment located in the project root folder to run robot tests.

**Architecture**
Always update the ARCHITECTURE.md file when changing the architecture of the project.
Document new components and their interactions in the ARCHITECTURE.md file.
- Table with exercise details (name, description, assigned helper)
- Confirmation prompt before deletion
- Redirect to exercises list after deletion
- track in the architecture the sites and the corresponding selenium tests

**Selenium Tests**
Selenium tests should be organized according to the pages they test.
Each page should have its own test file named after the page (e.g., test_exercises_page.py for Exercises Page).
Tests should cover all functionalities of the page, including role-based access control.
Use page object model to structure selenium tests for better maintainability.




