from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Seatchart(db.Model):
    __tablename__ ='seatchart'
    id = db.Column(db.Integer, primary_key=True)
    column1 = db.Column(db.String(5))
    column2 = db.Column(db.String(5))
    column3 = db.Column(db.String(5))
    column4 = db.Column(db.String(5))
    column5 = db.Column(db.String(5))
    column6 = db.Column(db.String(5))

#class Reservation(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(20), nullable=False)
#    seat_number = db.Column(db.Integer, nullable=False)

