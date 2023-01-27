from flask_login import UserMixin
from . import db
class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    role = db.Column(db.String(5))

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(10))
    row = db.Column(db.String(10))
    column = db.Column(db.String(10))
    seat_id = db.Column(db.String(10))
    status = db.Column(db.String(10))
    def serialize(self):
        return {
            'seat_id': self.seat_id,
            'status': self.status,
            'airline': self.airline
        }
