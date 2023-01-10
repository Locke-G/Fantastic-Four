from flask_login import UserMixin
from . import db
class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_id = db.Column(db.String(10), unique=True)
    row = db.Column(db.String(10))
    column = db.Column(db.String(10))
    status = db.Column(db.String(10))
