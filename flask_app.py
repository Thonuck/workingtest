
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, url_for
from database import Starter, Base, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///workingtest.db'  # Adjust the database URL as needed
db = SQLAlchemy(model_class=Base)
db.init_app(app)

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
        print("post")
        return render_template("starter.html", title="Starter")
    # read all starters from the database
    # and pass them to the template
    engine = create_engine('sqlite:///starters.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    starters = session.query(Starter).all()
    session.close()
    # Pass the starters to the template
    print(starters)
    return render_template("starter.html", title="Starter", starters=starters)
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

@app.route('/starter_details', methods=['GET', 'POST'])
def starter_details():
    if request.method == 'POST':
        # Handle form submission or other POST logic here
        starter_details = {"given_name": request.form.get('given_name'),
                           "family_name": request.form.get('family_name'),
                           "dog_name": request.form.get("dog_name"),
                           "dog_breed": request.form.get("dog_breed"),
                           "notes": request.form.get("notes"),
                           "payment_status": request.form.get("payment_status"),
                           "attendance_status": request.form.get("attendance_status")}

        # Create a new StarterModel instance
        new_starter = Starter(
            given_name=starter_details['given_name'],
            family_name=starter_details['family_name'],
            dog_name=starter_details['dog_name'],
            dog_breed=starter_details['dog_breed'],
            notes=starter_details['notes'],
            payment_status=bool(starter_details['payment_status']),
            attendance_status=bool(starter_details['attendance_status'])
        )
        # Create a new database session
        engine = create_engine('sqlite:///starters.db')  # Adjust the database URL as needed
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        # Add the new starter to the session and commit
        session.add(new_starter)
        session.commit()
        # Get the ID of the newly inserted starter
        starter_id = new_starter.id
        # Close the session
        session.close()

        if not starter_id:
            # Handle the case where the insertion failed
            return render_template("starter.html", title="Starter Details", error="Failed to insert starter details.")
        # Redirect to the starter details page or render a success message
        # For simplicity, we will just render the starter details page
        # You might want to redirect to a specific page or show a success message
        # For now, we will just render the starter details page
        # If you want to redirect, you can use:
        return redirect(url_for('starter_details', starter_id=starter_id))

        # return render_template("starter.html", title="Starter Details")

    return render_template("starter_details.html", title="Starter Details")