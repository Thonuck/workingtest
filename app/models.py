from app import db  # ✅ Normaler Import am Anfang!
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='guest')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # guest, organizer, helper

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
    max_points = db.Column(db.Integer, default=100, nullable=False)
    
    # Relationships
    competition = db.relationship('Competition', backref=db.backref('exercises', lazy=True))
    judge = db.relationship('User', foreign_keys=[judge_id], backref=db.backref('judged_exercises', lazy=True))
    helper = db.relationship('User', foreign_keys=[helper_id], backref=db.backref('helped_exercises', lazy=True))


# Exercise Point Entry model - for helpers to enter points
class ExercisePointEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    starter_id = db.Column(db.Integer, db.ForeignKey('starter.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relationships
    exercise = db.relationship('Exercise', backref=db.backref('point_entries', lazy=True))
    starter = db.relationship('Starter', backref=db.backref('point_entries', lazy=True))


# Exercise Result model - for final results
class ExerciseResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    starter_id = db.Column(db.Integer, db.ForeignKey('starter.id'), nullable=False)
    points = db.Column(db.Integer, nullable=True)
    published = db.Column(db.Boolean, default=False)
    
    # Relationships
    exercise = db.relationship('Exercise', backref=db.backref('results', lazy=True))
    starter = db.relationship('Starter', backref=db.backref('exercise_results', lazy=True))


# Update Competition model to track publication status
class CompetitionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False, unique=True)
    published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime, nullable=True)
    
    # Relationship
    competition = db.relationship('Competition', backref=db.backref('result_status', uselist=False))