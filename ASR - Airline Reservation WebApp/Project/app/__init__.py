from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
import sqlite3
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Wr5U92$&*68VoD29vbm4i!#m3#%&vq62@5UPN958%H!%f'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.config['ALLOWED_EXTENSIONS'] = ['.txt']
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
    app.config['SQLALCHEMY_POOL_SIZE'] = 5
    db.init_app(app)


    # If access is unauthorized it will redirect you to the loginpage
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # read textfile into list
    #data_list = []
    #with open( 'data/chartIn.txt') as f:
    #    file_data = f.readlines()
    #    for i in range(1, len(file_data)):
    #        data_lists = file_data[i].replace('F\n', 'F').split("\t")
    #        data_tuple = tuple(data_lists)
    #        data_list.append(data_tuple)
    # create cursor object
    #cursor = db.cursor()
    # create tablenames
    #cursor.execute("create table df (row_number integer, window_A text,"
    #               " middle_B text, aisle_C text, aisle_D text, middle_E text, middle_F text)")
    # read data to df
    #cursor.executemany('insert into df values (?,?,?,?,?,?,?)', data_list)
    #db.commit()

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user
        # table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app