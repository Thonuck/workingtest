from app import db
from flask_login import UserMixin
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(150), unique=True, nullable=False)
    password_hash = db.Column(String(512), nullable=False)
    role = db.Column(String(50), nullable=False, default='guest')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Person(db.Model):
    id = db.Column(Integer, primary_key=True)
    given_name = db.Column(String(100), nullable=False)
    family_name = db.Column(String(100), nullable=False)
    email = db.Column(String(120), nullable=True)


# Competition model
class Competition(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    level = db.Column(String(10), nullable=False)  # A, F, O
    location = db.Column(String(100), nullable=False)
    date = db.Column(Date, nullable=False)


# Dog model
class Dog(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    breed = db.Column(String(100), nullable=False)
    kennel = db.Column(String(100), nullable=True)


# Starter model
class Starter(db.Model):
    id = db.Column(Integer, primary_key=True)
    starter_number = db.Column(String(10), nullable=True)
    person_id = db.Column(Integer, ForeignKey('person.id'), nullable=True)
    dog_id = db.Column(Integer, ForeignKey('dog.id'), nullable=True)
    competition_id = db.Column(Integer, ForeignKey('competition.id'), nullable=True)
    paid = db.Column(Boolean, default=False)
    present = db.Column(Boolean, default=False)
    notes = db.Column(Text, nullable=True)

    # Relationships — each relationship is backed by its corresponding FK column above
    person = relationship('Person', foreign_keys=[person_id], backref=db.backref('starters', lazy=True))
    dog = relationship('Dog', foreign_keys=[dog_id], backref=db.backref('starters', lazy=True))
    competition = relationship('Competition', foreign_keys=[competition_id], backref=db.backref('starters', lazy=True))


# Exercise model
class Exercise(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    competition_id = db.Column(Integer, ForeignKey('competition.id'), nullable=False)
    judge_id = db.Column(Integer, ForeignKey('user.id'), nullable=True)
    helper_id = db.Column(Integer, ForeignKey('user.id'), nullable=True)
    max_points = db.Column(Integer, default=100, nullable=False)

    # Relationships
    competition = relationship('Competition', backref=db.backref('exercises', lazy=True))
    judge = relationship('User', foreign_keys='Exercise.judge_id', backref=db.backref('judged_exercises', lazy=True))
    helper = relationship('User', foreign_keys='Exercise.helper_id', backref=db.backref('helped_exercises', lazy=True))


# Exercise Point Entry model - for helpers to enter points
class ExercisePointEntry(db.Model):
    id = db.Column(Integer, primary_key=True)
    exercise_id = db.Column(Integer, ForeignKey('exercise.id'), nullable=False)
    starter_id = db.Column(Integer, ForeignKey('starter.id'), nullable=False)
    points = db.Column(Integer, nullable=False)
    notes = db.Column(Text, nullable=True)
    created_at = db.Column(DateTime, nullable=False, default=func.now())
    updated_at = db.Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    exercise = relationship('Exercise', backref=db.backref('point_entries', lazy=True))
    starter = relationship('Starter', backref=db.backref('point_entries', lazy=True))


# Exercise Result model - for final results
class ExerciseResult(db.Model):
    id = db.Column(Integer, primary_key=True)
    exercise_id = db.Column(Integer, ForeignKey('exercise.id'), nullable=False)
    starter_id = db.Column(Integer, ForeignKey('starter.id'), nullable=False)
    points = db.Column(Integer, nullable=True)
    published = db.Column(Boolean, default=False)

    # Relationships
    exercise = relationship('Exercise', backref=db.backref('results', lazy=True))
    starter = relationship('Starter', backref=db.backref('exercise_results', lazy=True))


# Update Competition model to track publication status
class CompetitionResult(db.Model):
    id = db.Column(Integer, primary_key=True)
    competition_id = db.Column(Integer, ForeignKey('competition.id'), nullable=False, unique=True)
    published = db.Column(Boolean, default=False)
    published_at = db.Column(DateTime, nullable=True)  # Set when published=True

    # Relationship
    competition = relationship('Competition', backref=db.backref('result_status', uselist=False))
