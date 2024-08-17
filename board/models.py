from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    surname = db.Column(db.String(1000))
    school = db.Column(db.String(100))
    role = db.Column(db.String(50))

class Flashcard(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100))
    definition = db.Column(db.String(1000))
    course = db.Column(db.String(100))