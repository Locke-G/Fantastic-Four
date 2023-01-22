import os
from flask import Blueprint,render_template, request, redirect, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Seat, User
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
                    seat = Seat(seat_id=seat_id, status='available', airline=root, row=row, column=column)
                    db.session.add(seat)
            db.session.commit()
        flash('File uploaded and processed')
        return redirect(url_for('main.upload'))
    return render_template('booking/upload.html')


@main.route('/select_airline', methods=['GET', 'POST'])
def select_airline():
    if request.method == 'POST':
        selected_airline = request.form.get('airline_select')
        seats = Seat.query.filter_by(airline=selected_airline).all()
        max_row = max(seat.row for seat in seats)
        max_col = max(ord(seat.column) - ord('A') for seat in seats)
        seat_chart = [['' for _ in range(max_col+1)] for _ in range(max_row+1)]
        for seat in seats:
            seat_chart[seat.row-1][ord(seat.column) - ord('A')] = seat.seat_id
    else:
        selected_airline = db.session.query(Seat.airline).distinct().first()[0]
        seats = Seat.query.filter(Seat.airline == selected_airline).all()
        max_row = max(seat.row for seat in seats)
        max_col = max(ord(seat.column) - ord('A') for seat in seats)
        #TypeError: can only concatenate str (not "int") to str
        seat_chart = [['' for _ in range(max_col+1)] for _ in range(max_row+1)]
        for seat in seats:
            seat_chart[seat.row-1][ord(seat.column) - ord('A')] = seat.seat_id

    airlines = db.session.query(Seat.airline).distinct()
    return render_template(
        'booking/select_airline.html',
        airlines=airlines,
        seat_chart=seat_chart,
        selected_airline=selected_airline
    )


