from flask import Blueprint, Flask, render_template, request, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from .models import Seatchart

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
def uploadseatfile():
    # If the request method is 'POST', the user has submitted the form
    if request.method == 'POST':
        # Get the file from the request
        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return redirect(url_for('upload'))

        # Read the contents of the file and parse it into a list of values
        lines = file.readlines()
        values = []
        for line in lines:
            parts = line.strip().split('\t')
            values.append(
                Seatchart(column1=parts[0], column2=parts[1], column3=parts[2],
                          column4=parts[3], column5=parts[4],column6=parts[5]))

        # Add the values to the database
        session = Session()
        session.add_all(values)
        session.commit()
        session.close()
        return 'Seat chart data added to database!'
    return render_template('booking/upload.html')

