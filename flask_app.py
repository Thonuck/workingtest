# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from blueprints.main.routes import main_bp
from blueprints.organizer.routes import organizer_bp
from blueprints.helper.routes import helper_bp
from config import Config
from extensions import init_extensions
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # guest, organizer, helper

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    given_name = db.Column(db.String(100), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)

# Competition model
class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(10), nullable=False)  # A, F, O
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

# Dog model
class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    kennel = db.Column(db.String(100), nullable=True)

# Starter model
class Starter(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    person_id: int = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    dog_id: int = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    competition_id: int = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    paid: bool = db.Column(db.Boolean, default=False)
    present: bool = db.Column(db.Boolean, default=False)
    notes: str = db.Column(db.Text, nullable=True)

# Exercise model
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    judge_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    helper_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    init_extensions(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(organizer_bp, url_prefix='/organizer')
    app.register_blueprint(helper_bp, url_prefix='/helper')

    return app


if __name__ == '__main__':
    app: Flask = create_app()
    app.run(debug=True)
