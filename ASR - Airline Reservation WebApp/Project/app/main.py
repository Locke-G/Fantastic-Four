import os
from flask import Blueprint,render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from functools import wraps
from .models import Seat, User
from . import db


main = Blueprint('main', __name__)

# add user roles decorator with @role_required('admin')
# so that admins or other defined roles only
# have access to certain routes
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('booking/profile.html', name=current_user.name)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Check file extension
        if not file or '.txt' not in file.filename:
            flash('File type not supported')
            return redirect(request.url)

        # Save the file
        file = request.files['file']
        if file:
            filename = file.filename
            root, ext = os.path.splitext(filename)
            file.seek(0)
            lines = file.read().decode().split("\n")
            for i, line in enumerate(lines[1:]):
                cells = line.strip().split("\t")
                for j, cell in enumerate(cells[1:]):
                    seat_id = str(i + 1) + chr(ord('A') + j)
                    row = int(seat_id[:-1])
                    column = seat_id[-1]
                    seat = Seat(
                        seat_id=seat_id,
                        status='available',
                        airline=root,
                        row=row,
                        column=column
                    )
                    db.session.add(seat)
            db.session.commit()
        flash('File uploaded and processed')
        return redirect(url_for('main.upload'))
    return render_template('booking/upload.html')

@main.route('/seats', methods=['GET', 'POST'])
@login_required
def seats():
    airlines = db.session.query(Seat.airline).distinct().all()
    if request.method == 'POST':
        airline = \
            request.form.get('airline')
        reserved_seats = \
            Seat.query.filter(Seat.status == 'reserved',Seat.airline == airline).all()
        rows = \
            db.session.query(Seat.row).distinct().filter_by(airline=airline).all()
        columns = \
            db.session.query(Seat.column).distinct().filter_by(airline=airline).all()
        reserved_seats = \
            {f'{seat.row}{seat.column}': seat.status for seat in reserved_seats}
        selected_airline = \
            airline
    else:
        airlines = db.session.query(Seat.airline).distinct().all()
        reserved_seats = []
        rows = []
        columns = []
        selected_airline = ""
    return render_template(
        'booking/seats.html',
        airlines=airlines,
        reserved_seats=reserved_seats,
        rows=rows,
        columns=columns,
        selected_airline=selected_airline
    )

@main.route('/reserve-seat', methods=['POST'])
@login_required
@role_required('admin')
def reserve_seat():
    # Get's the input of reserved seat from User for the current
    seat_id = request.form.get('seat_id').upper()
    airline = request.form.get('airline')
    fullname = request.form.get('fullname')
    seat = Seat.query.filter_by(seat_id=seat_id, airline=airline).first()
    # Checks if seat.status is already reserved
    if seat:
        if seat.status == 'reserved':
            flash('Seat is already reserved. Please select a different one.')
            return redirect(url_for('main.seats'))
        # if not reserved seat gets reserved
        else:
            # if Optional name is entered that is used in the database
            seat.status = 'reserved'
            if fullname:
                seat.name = fullname
                seat.username = current_user.username
            # if no name is given username from account is used
            else:
                seat.name = current_user.name
                seat.username = current_user.username
            db.session.commit()
            flash('Seat reserved successfully')
            return redirect(url_for('main.seats'))
    else:
        flash('Seat not found. Please try again')
        return redirect(url_for('main.seats'))

@main.route('/reserved_seats', methods=['GET', 'POST'])
def reserved_seats():
    if request.method == 'POST':
        selected_airline = request.form['airline']
    else:
        selected_airline = ''
    airlines = get_all_airlines() # function that returns a list of all airlines
    seats = get_all_seats(selected_airline) # function that returns a list of all seats for the selected airline
    reserved_seats = get_reserved_seats(selected_airline) # function that returns a dictionary of reserved seats for the selected airline

    rows = list(string.ascii_uppercase)[:get_num_rows(selected_airline)] # function that returns the number of rows for the selected airline
    columns = range(1, get_num_columns(selected_airline) + 1) # function that returns the number of columns for the selected airline

    return render_template('reserved_seats.html', selected_airline=selected_airline, airlines=airlines, rows=rows, columns=columns, reserved_seats=reserved_seats)

@main.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    seat_id = request.form['seat_id']
    #cancel_seat_reservation(seat_id) # function that cancels the reservation for the given seat_id
    flash("Seat reservation canceled")
    return redirect(url_for('main.reserved_seats'))


import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Use the logging module to log a message
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')