# ReadMe
## _ASR - Airplain Reservation WebApp_

This Web application is build upon Flask Framework in Python  and is part
of the Final Project for the Lecture _Programming for Data Scientists: Python_
in Georg-August-Universität Göttingen.

## Goals

- A realtional database for data storage 
- A web-based frontend
- A computing backend implemented in Python

## Features

- Reading the seat chart from an txt file and displaying them
- User Login/Signup/Logout with 4 Users one of which being an Admin
- Displaying the seat in a
- ...

# Build the application

### Step 1 - Clone the application

```sh
$ # git clone https://github.com/...
$ cd ASR\ -\ Airline\ Reservation\ WebApp/Project/
```

### Step 2 - Create virtual environment

 ```sh
$ pyhton3 -m venv auth
$ source auth/bin/activate
 ```

### Step 3 - Install the required packages

 ```sh
 $ pip install -r requirements.txt
 ```

### Step 4 - Set Up the virtual environment
```sh
$ export FLASK_APP=app
$ #Add debugger if required
$ export FLASK_DEBUG=1
```
