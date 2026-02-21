from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from app import db  # ✅ Normaler Import am Anfang!
from flask_login import UserMixin
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(150), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default='guest')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Person(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    given_name: Mapped[str] = mapped_column(String(100), nullable=False)
    family_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)


# Competition model
class Competition(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(10), nullable=False)  # A, F, O
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)


# Dog model
class Dog(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    breed: Mapped[str] = mapped_column(String(100), nullable=False)
    kennel: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)


# Starter model
class Starter(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('person.id'), nullable=True)
    dog_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('dog.id'), nullable=True)
    competition_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('competition.id'), nullable=True)
    paid: Mapped[bool] = mapped_column(Boolean, default=False)
    present: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    person: Mapped[Optional[Person]] = relationship('Person', backref=db.backref('starters', lazy=True))
    dog: Mapped[Optional[Dog]] = relationship('Dog', backref=db.backref('starters', lazy=True))
    competition: Mapped[Optional[Competition]] = relationship('Competition', backref=db.backref('starters', lazy=True))


# Exercise model
class Exercise(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    competition_id: Mapped[int] = mapped_column(Integer, ForeignKey('competition.id'), nullable=False)
    judge_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    helper_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    max_points: Mapped[int] = mapped_column(Integer, default=100, nullable=False)

    # Relationships
    competition: Mapped[Competition] = relationship('Competition', backref=db.backref('exercises', lazy=True))
    judge: Mapped[Optional[User]] = relationship('User', foreign_keys='Exercise.judge_id', backref=db.backref('judged_exercises', lazy=True))
    helper: Mapped[Optional[User]] = relationship('User', foreign_keys='Exercise.helper_id', backref=db.backref('helped_exercises', lazy=True))


# Exercise Point Entry model - for helpers to enter points
class ExercisePointEntry(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey('exercise.id'), nullable=False)
    starter_id: Mapped[int] = mapped_column(Integer, ForeignKey('starter.id'), nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    exercise: Mapped[Exercise] = relationship('Exercise', backref=db.backref('point_entries', lazy=True))
    starter: Mapped[Starter] = relationship('Starter', backref=db.backref('point_entries', lazy=True))


# Exercise Result model - for final results
class ExerciseResult(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey('exercise.id'), nullable=False)
    starter_id: Mapped[int] = mapped_column(Integer, ForeignKey('starter.id'), nullable=False)
    points: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    published: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    exercise: Mapped[Exercise] = relationship('Exercise', backref=db.backref('results', lazy=True))
    starter: Mapped[Starter] = relationship('Starter', backref=db.backref('exercise_results', lazy=True))


# Update Competition model to track publication status
class CompetitionResult(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competition_id: Mapped[int] = mapped_column(Integer, ForeignKey('competition.id'), nullable=False, unique=True)
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Set when published=True

    # Relationship
    competition: Mapped[Competition] = relationship('Competition', backref=db.backref('result_status', uselist=False))
