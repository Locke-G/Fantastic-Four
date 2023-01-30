from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from .models import User, Seat
from . import db
import matplotlib.pyplot as plt
import io
import base64

# Create blueprint for stats route
stats = Blueprint('stats', __name__)

# Decorator to check if user has the required role
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                # Redirect to main index if user doesn't have required role
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Route to display graph of seat availability and reservation
@stats.route('/graph1', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def graph_seats():
    # Get all unique airlines
    airlines = db.session.query(Seat.airline).distinct().all()
    airlines = [airline[0] for airline in airlines]

    # Get number of reserved and available seats for each airline and save them as a dictionary
    reserved_seats = {}
    available_seats = {}
    for airline in airlines:
        reserved = Seat.query.filter(Seat.status == 'reserved', Seat.airline == airline).count()
        available = Seat.query.filter(Seat.status == 'available', Seat.airline == airline).count()
        reserved_seats[airline] = reserved
        available_seats[airline] = available

    # Plot bar graphs of reserved and available seats
    fig = plt.figure()
    fig.set_size_inches(15.5, 10.5)
    plt.subplots_adjust(left=0.2, bottom=0.3)
    plt.subplot(1, 2, 1)
    plt.bar(reserved_seats.keys(), reserved_seats.values(), label="Reserved", color='#e70d0d')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.bar(available_seats.keys(), available_seats.values(), label="Available", color='#69dc1d')
    plt.legend()

    # Create table with data
    cellText = []
    for airline, reserved in reserved_seats.items():
        # Calculate percentage of reserved and available seats
        available_per = (available_seats[airline] / (available_seats[airline] + reserved_seats[airline])) * 100
        available = available_seats[airline]
        reserved_per = (reserved_seats[airline] / (available_seats[airline] + reserved_seats[airline])) * 100
        cellText.append([airline, reserved, round(reserved_per, 2), available, round(available_per, 2)])
    table = plt.table(cellText=cellText, colLabels=[
        "Airline",
        "Reserved",
        "Reserved [%]",
        "Available",
        "Available [%]"
    ], loc='top')
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
    seats = Seat.query.all()
    airlines = db.session.query(Seat.airline).distinct().all()
    airlines = [airline[0] for airline in airlines]
    statuses = db.session.query(Seat.status).distinct().all()
    statuses = [status[0] for status in statuses]
    return render_template("stats/table_seats.html", seats=seats, airlines=airlines, statuses=statuses)


# create a new route for the user table
@stats.route('/userinfo')
def userinfo():
    # query the User model to get all the data
    users = User.query.all()
    # pass the data to the template
    return render_template('stats/Userinfo.html', users=users)






