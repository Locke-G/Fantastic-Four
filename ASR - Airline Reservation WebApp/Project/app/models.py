from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

#class Inputdata(db.Model):
#    row_num = db.Column(db.Integer, primary_key=True)
#    wind_A = db.Column(db.String(1), notnull=True)
#    midd_B = db.Column(db.String(1), notnull=True)
#    aisl_C = db.Column(db.String(1), notnull=True)
#    aisl_D = db.Column(db.String(1), notnull=True)
#    midd_E = db.Column(db.String(1), notnull=True)
#    wind_F = db.Column(db.String(1), notnull=True)

