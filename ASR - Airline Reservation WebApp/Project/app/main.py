import os
import logging
from flask import Blueprint,render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from functools import wraps
from .models import Seat, User
from . import db

# Blueprint definition for main module
main = Blueprint('main', __name__)

# Setup basic logging configuration
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Decorator to check if user role matches the required role
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Redirect user to index if their role is not the required role
            if current_user.role != role:
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Route for the index page
@main.route('/')
def index():
    return render_template('index.html')

# Route for the profile page, requires user to be logged in
@main.route('/profile')
@login_required
def profile():
    return render_template('booking/profile.html', name=current_user.name)

# Route for uploading a file, requires user to be logged in and have an 'admin' role
@main.route('/upload', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def upload():
    if request.method == 'POST':
        # Check if file was submitted
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        # Check file extension
        if not file or '.txt' not in file.filename:
            flash('File type not supported', 'error')
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
        flash('File uploaded and processed', 'success')
        return redirect(url_for('main.upload'))
    return render_template('booking/upload.html')

@main.route('/seats', methods=['GET', 'POST'])
@login_required
def seats():
    # Get unique airlines from the seats table
    airlines = db.session.query(Seat.airline).distinct().all()
    if request.method == 'POST':
        # Get the selected airline
        airline = request.form.get('airline')
        # Get all the reserved seats of the selected airline
        reserved_seats = Seat.query.filter(
            Seat.status == 'reserved',
            Seat.airline == airline
        ).all()
        # Get unique rows of the selected airline
        rows = db.session.query(Seat.row)\
            .distinct().filter_by(airline=airline).all()
        # Get unique columns of the selected airline
        columns = db.session.query(Seat.column)\
            .distinct().filter_by(airline=airline).all()
        # Create a dictionary of the reserved seats
        reserved_seats = {f'{seat.row}{seat.column}': seat.status for seat in reserved_seats}
        selected_airline = airline
    else:
        # Get unique airlines from the seats table
        airlines = db.session.query(Seat.airline).distinct().all()
        reserved_seats = []
        rows = []
        columns = []
        selected_airline = ""
    # Render the seats.html template
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
def reserve_seat():
    # Get the selected seat, airline, and fullname from the form
    seat_id = request.form.get('seat_id').upper()
    airline = request.form.get('airline')
    fullname = request.form.get('fullname')
    # Get the selected seat from the database
    seat = Seat.query.filter_by(seat_id=seat_id, airline=airline).first()
    if seat:
        # Check if the seat is already reserved
        if seat.status == 'reserved':
            flash('Seat is already reserved. Please select a different one.', 'error')
            return redirect(url_for('main.seats'))
        # Reserve the seat
        else:
            seat.status = 'reserved'
            # If a fullname is provided, use it. Otherwise, use the username
            if fullname:
                seat.name = fullname
                seat.username = current_user.username
            else:
                seat.name = current_user.name
                seat.username = current_user.username
            db.session.commit()
            flash('Seat reserved successfully', 'success')
            return redirect(url_for('main.seats'))
    else:
        flash('Seat not found. Please try again', 'error')
        return redirect(url_for('main.seats'))

# Route to cancel reservation
@main.route('/cancel_reservation', methods=['POST', 'GET'])
@login_required
@role_required('admin')
def cancel_reservation():
    # Get all distinct airlines from seat table
    airlines = db.session.query(Seat.airline).distinct().all()

    # Check if request method is POST
    if request.method == 'POST':
        # Get the selected airline from the form
        selected_airline = request.form.get('airline')

        # Get all reserved seats for the selected airline
        reserved_seats = Seat.query.filter(
            Seat.status == 'reserved',
            Seat.airline == selected_airline
        ).values(
            Seat.seat_id,
            Seat.username,
            Seat.name,
            Seat.airline
        )
    else:
        # No airline selected, get all reserved seats
        selected_airline = None
        reserved_seats = Seat.query.filter(
            Seat.status == 'reserved'
        ).values(
            Seat.seat_id,
            Seat.username,
            Seat.name,
            Seat.airline
        )

    # Render the cancel_reservation.html template with the seat information
    return render_template(
        'booking/cancel_reservation.html',
        can_reserved_seats=reserved_seats,
        airlines=airlines,
        selected_airline=selected_airline
    )

# Route to delete a reservation
@main.route('/delete_reservation/<string:seat_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_reservation(seat_id):
    # Get the selected airline from the form
    selected_airline = request.form.get("airline")

    # Get the seat with the specified seat_id and selected airline
    seat = Seat.query.filter_by(airline=selected_airline, seat_id=seat_id).first()

    # If seat is found
    if seat:
        # Change the status of the seat to available
        seat.status = 'available'
        seat.name = None
        seat.username = None
        flash("Reservation was canceled", 'success')
        # Commit changes to the database
        db.session.commit()
    else:
        # Seat not found, flash a message
        flash("Seat not found", 'error',)

    # Redirect to the cancel_reservation page
    return redirect(url_for('main.cancel_reservation'))

# Log messages for testing purposes
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
