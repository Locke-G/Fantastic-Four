from flask import Blueprint, Flask, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from .models import Seat, User
import sys
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('booking/profile.html', name=current_user.name)

# Debug logging hiinzufügen
@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Get the file from the form input
        file = request.files['file']
        # Check if the file is of a valid type
        if not file or not allowed_file(file.filename):
            flash('Invalid file format. Please upload a .txt file')
            return redirect(url_for('main.upload'))
        # Save the file to the server
        filename = secure_filename(file.filename)
        file.save('' + filename)
        # Read the file into a pandas dataframe
        data = pd.read_csv('' + filename, delimiter=' ')
        flash(data.to_string())
        # Iterate through the dataframe, creating Seat objects and adding them to the database
        for i, row in data.iterrows():
            print(row, file=sys.stderr)
            seat_id = row['row'] + row['column']
            seat = Seat(seat_id=seat_id, row=row['row'], column=row['column'], status='available')
            db.session.add(seat)
        db.session.commit()
        flash('File uploaded and data stored in database')
        return redirect(url_for('main.index'))
    return render_template('booking/upload.html')
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in 'txt'


@main.errorhandler(413)
def file_too_large(e):
    return "File too large", 413



