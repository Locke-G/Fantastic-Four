from flask import Blueprint, Flask, render_template, request, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
import pandas as pd

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

            # Read the contents of the file into a DataFrame using pandas
            df = pd.read_csv(file, delimiter='\t')

            # Obtain the filename of the uploaded file
            filename = secure_filename(file.filename)

            # Extract the name of the file and remove the file extension
            table_name = filename.split(".")[0]

            # Save the DataFrame to a SQL table in the database with the name of the file
            df.to_sql(table_name, db.engine)
            return f'Data of {table_name} added to the database!'
    return render_template('booking/upload.html')

@main.errorhandler(413)
def file_too_large(e):
    return "File too large", 413



