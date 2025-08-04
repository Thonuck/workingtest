
"""
This module provides a class for connecting to a SQLite database.

the database is handled by using sqlalchemie. It provides the base implementation for:
Starter:
- given_name
- family_name
- dog_name
- notes
- payent_status
- attendance_status

"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

# create the sqlite database engine, if it doen't exist it will be created
# def create_db():
#     engine = create_engine('sqlite:///starters.db')  # Adjust the database URL as needed
#     Base.metadata.create_all(engine, echo=True)  # Create tables if they don't exist
#     return engine

class Base(DeclarativeBase):
    pass

class Starter(Base):
    __tablename__ = 'starters'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    given_name: Mapped[str] = mapped_column(String(30))
    family_name: Mapped[str] = mapped_column(String(30))
    dog_name: Mapped[str] = mapped_column(String(30))
    dog_breed: Mapped[str] = mapped_column(String(30))
    notes: Mapped[str] = mapped_column(String(120))
    payment_status: Mapped[str] = mapped_column(String(30))
    attendance_status: Mapped[str] = mapped_column(String(30))

    def __repr__(self):
        return f"<StarterModel(id={self.id}, given_name={self.given_name}, family_name={self.family_name}>"