from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    #User input is requested
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    #Check if user actually exists
    user = User.query.filter_by(username=username).first()
    #If Username or user supplied password(hashed) doesn't
    #match in the database error is returned
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    #User input is requested
    email = request.form.get('email')
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    # if this returns a usererx, then the email
    # or username already exists in database
    userer1 = User.query.filter_by(email=email).first()
    userer2 = User.query.filter_by(username=username).first()
    # if an email is found, we want to redirect back to signup
    if userer1:
        flash('Email address already exists. Try again.')
        return redirect(url_for('auth.signup'))
    # if a user is found, we want to redirect back to signup
    if userer2:
        flash('Username already exists. Try again.')
        return redirect(url_for('auth.signup'))
    # if passwords dont match, redirect to signup
    if password != password2:
        flash('Passwords must match!!!')
        return redirect(url_for('auth.signup'))
    # create new user with the form data.
    # Hash the password so plaintext version isn't saved.
    new_user = User(email=email, username=username, name=name,
                    password=generate_password_hash(password, method='sha256'))
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    #redirects to login page after successful signup
    return redirect(url_for('auth.login'))

#create a logout Page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out. Hope to see you soon')
    return redirect(url_for('auth.login'))
