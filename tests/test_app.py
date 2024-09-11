import unittest
from flask import Flask
from app import app  # Import the Flask app from your main app file
import mysql.connector
from unittest.mock import patch

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.cursor')  # Mocking the MySQL cursor
    def test_form_page_loads(self, mock_cursor):
        # Test if the form page loads successfully
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Employee Entry Form', response.data)  # Assuming this text is in the form.html

    @patch('app.cursor')  # Mocking the MySQL cursor
    def test_submit_form_success(self, mock_cursor):
        # Simulate a successful form submission
        response = self.app.post('/submit_form', data={
            'employee_id': '12345',
            'first_name': 'John',
            'last_name': 'Doe',
            'department': 'IT',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'date_of_joining': '2024-09-01'
        })

        # Check if the form redirects after submission
        self.assertEqual(response.status_code, 302)  # Redirect status code

    @patch('app.cursor')  # Mocking the MySQL cursor
    def test_submit_form_db_insert(self, mock_cursor):
        # Test that the correct SQL query is executed upon form submission
        self.app.post('/submit_form', data={
            'employee_id': '12345',
            'first_name': 'John',
            'last_name': 'Doe',
            'department': 'IT',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'date_of_joining': '2024-09-01'
        })

        # Check if the cursor.execute() was called with the correct SQL and values
        mock_cursor.execute.assert_called_with(
            "INSERT INTO employees (employee_id, first_name, last_name, department, email, phone, date_of_joining) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            ('12345', 'John', 'Doe', 'IT', 'john.doe@example.com', '1234567890', '2024-09-01')
        )

if __name__ == '__main__':
    unittest.main()
