
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html", title="Workingtest Planer")

@app.route('/starter', methods=['GET', 'POST'])
def starter():
    """
    Starter page for the Workingtest Planner application.
    """
    # If you want to handle POST requests, you can add logic here.
    if request.method == 'POST':
        # Handle form submission or other POST logic here
        return render_template("starter.html", title="Starter")
    return render_template("starter.html", title="Starter")

@app.route('/tasks')
def tasks():
    return render_template("tasks.html", title="Aufgaben")

@app.route('/helpers')
def helpers():
    return render_template("helpers.html", title="Aufgaben")

@app.route('/about')
def about():
    return render_template("index_boot.html", title="Aufgaben")

@app.route('/new_working_test')
def new_working_test():
    return render_template("new_working_test.html", title="Neuer Working Test")

@app.route('/starter_details')
def starter_details():
    return render_template("starter_details.html", title="Starter Details")