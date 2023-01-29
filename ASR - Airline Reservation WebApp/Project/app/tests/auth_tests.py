import unittest
from flask import request
from flask_login import current_user
from app import create_app, db
from app.models import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        # Create a test user
        test_user = User(username='test_user', password='test_password')
        db.session.add(test_user)
        db.session.commit()

        # Test GET request
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

        # Test invalid POST request
        response = self.client.post('/login', data={
            'username': 'test_user',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)

        # Test valid POST request
        response = self.client.post('/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(current_user.is_authenticated)

    def test_signup(self):
        # Test GET request
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

        # Test invalid POST request (username already exists)
        response = self.client.post('/signup', data={
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test_password',
            'password2': 'test_password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertEqual(User.query.count(), 1)

        # Test valid POST request
        response = self.client.post('/signup', data={
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'new_password',
            'password2': 'new_password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(current_user.is_authenticated)
        self.assertEqual(User.query.count(), 2)


if __name__ == '__main__':
    unittest.main()
