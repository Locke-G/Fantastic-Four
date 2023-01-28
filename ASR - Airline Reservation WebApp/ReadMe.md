# ReadMe
## _ASR - Airplain Reservation WebApp_

This Web application is build upon the Flask Framework in Python  and is part
of the Final Project for the Lecture _Programming for Data Scientists: Python_
in Georg-August-Universität Göttingen.

## Goals

- A realtional database for data storage 
- A web-based frontend
- A computing backend implemented in Python

## Motivation

- Final Project of Course

## Features

- Reading the seat chart from an txt file and displaying them
- User Login/Signup/Logout with 4 Users one of which being an Admin
- Displaying seat chart and showing available seats
- normal users can book a seat
- admin user can cancel seats
- admin user can see user information and statistics about available seats
- a help float text is available for the main functions

# Build the application

### Step 1 - Clone the application

```sh
$ git clone https://github.com/Locke-G/Fantastic-Four.git
$ cd ASR\ -\ Airline\ Reservation\ WebApp/Project/
```

### Step 2 - Create virtual environment

 ```sh
$ pyhton3 -m venv auth
$ # when on linux or mac OS 
$ source auth/bin/activate
$ # when on windows 
$ ./auth/Scripts/activate
 ```

### Step 3 - Install the required packages

 ```sh
 $ pip install -r requirements.txt
 ```

### Step 4 - Create the virtual environment
```sh
$ export FLASK_APP=app
$ #Add debugger if required
$ export FLASK_DEBUG=1
```
### Step 5 - Run the application
```sh
$ flask run
```

### Step 6 - Have fun!


## API Reference
https://flask.palletsprojects.com/en/2.2.x/#api-reference

## Licence
see Github licenceagreement.pdf









