from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form input
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        # Check if user exists and if password is correct
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid login credentials')
    return render_template('auth/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form input
        email = request.form.get('email')
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # Check if email or username is already taken
        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists')
        elif password != password2:
            flash('Passwords must match')
        else:
            # Create a new user and add it to the database
            new_user = User(
                email=email, username=username, name=name,
                password=generate_password_hash(password, method='sha256'),
                role='user'
                            )
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful, please log in.')
            return redirect(url_for('auth.login'))
    return render_template('auth/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out. Hope to see you soon')
    return redirect(url_for('auth.login'))
