import os
import unittest

from flask import request
from flask_login import current_user

from app import create_app, db
from app.models import Seat
from app.views.main import main

class SeatsViewTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_seats_route_GET(self):
        # Add a seat to the database
        seat = Seat(
            seat_id='1A',
            status='available',
            airline='Delta',
            row=1,
            column='A'
        )
        db.session.add(seat)
        db.session.commit()

        # Log in a user
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1

        # Send a GET request to the /seats route
        response = self.client.get('/seats', follow_redirects=True)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the airlines variable in the response contains the
        # unique airlines from the seats table
        self.assertEqual(len(response.json['airlines']), 1)
        self.assertEqual(response.json['airlines'][0]['airline'], 'Delta')

        # Assert that the reserved_seats variable in the response is an empty list
        self.assertEqual(response.json['reserved_seats'], [])

        # Assert that the rows variable in the response contains the unique rows
        # of the selected airline
        self.assertEqual(len(response.json['rows']), 1)
        self.assertEqual(response.json['rows'][0]['row'], 1)

        # Assert that the columns variable in the response contains the unique columns
        # of the selected airline
        self.assertEqual(len(response.json['columns']), 1)
        self.assertEqual(response.json['columns'][0]['column'], 'A')

        # Assert that the selected_airline variable in the response is an empty string
        self.assertEqual(response.json['selected_airline'], '')

    def test_seats_route_POST(self):
        # Add two seats to the database
        seat1 = Seat(
            seat_id='1A',
            status='available',
            airline='Delta',
            row=1,
            column='A'
        )
        seat2 = Seat(
            seat_id='1B',
            status='reserved',
            airline='Delta',
            row=2,
            column='B'
        )

        db.session.add(seat1)
        db.session.add(seat2)
        db.session.commit()

        # Log in a user
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1

        # Send a POST request to the /seats route with the selected airline
        response = self.client.post('/seats', data={'airline': 'Delta'}, follow_redirects=True)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the airlines variable in the response contains the
        # unique airlines from the seats table
        self.assertEqual(len(response.json['airlines']), 1)
        self.assertEqual(response.json['airlines'][0]['airline'], 'Delta')

        # Assert that the reserved_seats variable in the response contains
        # a dictionary of the reserved seats
        self.assertEqual(len(response.json['reserved_seats']), 1)
        self.assertEqual(response.json['reserved_seats']['1B'], 'reserved')

        # Assert that the rows variable in the response contains the unique rows
        # of the selected airline
        self.assertEqual(len(response.json['rows']), 1)
        self.assertEqual(response.json['rows'][0]['row'], 1)

        # Assert that the columns variable in the response contains the unique columns
        # of the selected airline
        self.assertEqual(len(response.json['columns']), 2)
        self.assertEqual(response.json['columns'][0]['column'], 'A')
        self.assertEqual(response.json['columns'][1]['column'], 'B')

        # Assert that the selected_airline variable in the response contains
        # the selected airline
        self.assertEqual(response.json['selected_airline'], 'Delta')


