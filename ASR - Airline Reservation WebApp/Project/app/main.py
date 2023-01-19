import os
from flask import Blueprint, Flask, render_template, request, redirect, flash, url_for
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
        if not file or '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in app.config['ALLOWED_EXTENSIONS']:
            flash('File type not supported')
            return redirect(request.url)

        # Check file size
        if file.content_length > app.config['MAX_CONTENT_LENGTH']:
            flash('File size exceeded')
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
                    seat = Seat(seat_id=seat_id, status='available', airline=root)
                    db.session.add(seat)
            db.session.commit()
        flash('File uploaded and processed')
        return redirect(url_for('main.upload'))
    return render_template('booking/upload.html')


