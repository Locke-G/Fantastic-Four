from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import wraps
from .models import User, Seat
from . import db
from matplotlib import pyplot as plt
import io
import base64
import pandas as pd

stats = Blueprint('stats', __name__)
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@stats.route('/graph1', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def graph_seats():
    global buf
    airlines = db.session.query(Seat.airline).distinct().all()
    airlines = [airline[0] for airline in airlines]
    reserved_seats = {}
    available_seats = {}
    for airline in airlines:
        reserved = Seat.query.filter(Seat.status == 'reserved', Seat.airline == airline).count()
        available = Seat.query.filter(Seat.status == 'available', Seat.airline == airline).count()
        reserved_seats[airline] = reserved
        available_seats[airline] = available
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.2, bottom=0.3)
    ax.bar(reserved_seats.keys(), reserved_seats.values(), label="Reserved")
    ax.bar(available_seats.keys(), available_seats.values(), label="Available")
    ax.legend()

    # Create table
    table_data = [['Airline', 'Reserved Seats', 'Available Seats']]
    cellText = []
    for airline, reserved in reserved_seats.items():
        available = available_seats[airline]
        cellText.append([airline, reserved, available])
    table = ax.table(cellText=cellText, colLabels=["Airline", "Reserved", "Available"], loc='bottom')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    imdata = base64.b64encode(buf.read()).decode("ascii")

    return render_template("stats/graph.html", mimetype="buf/png", cache_timeout=0, imdata=imdata)

@stats.route('/tables', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def tables():
    airlines = db.session.query(Seat.airline).distinct().all()
    airlines = [airline[0] for airline in airlines]
    reserved_seats = {}
    available_seats = {}
    for airline in airlines:
        reserved = Seat.query.filter(Seat.status == 'reserved', Seat.airline == airline).all()
        available = Seat.query.filter(Seat.status == 'available', Seat.airline == airline).all()
        reserved_seats[airline] = reserved
        available_seats[airline] = available
    return render_template("stats/table_seats.html", reserved_seats=reserved_seats, available_seats=available_seats)

# create a new route for the user table
@stats.route('/userinfo')
def userinfo():
    # query the User model to get all the data
    users = User.query.all()
    # pass the data to the template
    return render_template('stats/Userinfo.html', users=users)






