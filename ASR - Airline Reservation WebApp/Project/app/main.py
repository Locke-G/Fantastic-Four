import os
from flask import Blueprint, Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Seat
from . import db


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('booking/profile.html', name=current_user.name)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
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
        # not working cannot import app error
        #if not file or '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in app.config['ALLOWED_EXTENSIONS']:
        #    flash('File type not supported')
        #    return redirect(request.url)

        # Check file size
        # not working cannot import app error
        #if file.content_length > app.config['MAX_CONTENT_LENGTH']:
        #    flash('File size exceeded')
        #    return redirect(request.url)

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
                    seat = Seat(seat_id=seat_id, status='available', airline=root)
                    db.session.add(seat)
            db.session.commit()
        flash('File uploaded and processed')
        return redirect(url_for('main.upload'))
    return render_template('booking/upload.html')

@main.route('/select_airline', methods=['GET'])
def select_airline():
    airlines = db.session.query(Seat.airline).distinct()
    seats = Seat.query.all()
    return render_template('booking/select_airline.html', airlines=airlines, seats=seats)

@main.route('/get_seats', methods=['GET'])
def get_seats():
    airline = request.args.get("airline")
    seats = Seat.query.filter_by(airline=airline).all()
    return jsonify(seats=[seat.serialize() for seat in seats])

@main.route('/reserve_seat', methods=['POST'])
def reserve_seat():
    data = request.get_json()
    seat_id = data.get('seatId')
    seat = Seat.query.filter_by(seat_id=seat_id).first()
    if seat is None:
        return jsonify(success=False, message='Seat not found')
    if seat.status != 'available':
        return jsonify(success=False, message='Seat is not available')
    seat.status = 'reserved'
    db.session.commit()
    return jsonify(success=True)
