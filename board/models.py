from . import db
from flask_login import UserMixin

"""
User class for the login and signup process. Also used for profile.
Role decides whether to get directed to the student or teacher landing page
"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    surname = db.Column(db.String(1000))
    school = db.Column(db.String(100))
    role = db.Column(db.String(50))

"""
Flashcard class for creating flashcards of a certain course
Created by teacher, can be viewed by student
"""
class Flashcard(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100))
    definition = db.Column(db.String(1000))
    course = db.Column(db.String(100))

"""
Course Class for the course information to create course numbers and to redirect the right flashcards, the right students and the right teachers to the right course
Accessibility and security
"""
class Course(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100))
    course_number = db.Column(db.String(20))
    subject = db.Column(db.String(100))
    teacher = db.Column(db.String(100))

"""
Combines Course and Student information
"""

class RelationStudentCourse(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    course_id=db.Column(db.Integer)
    student_id=db.Column(db.Integer)