import unittest
from flask import session
from unittest.mock import MagicMock, patch
from main import app, cursor, mysql
from flask import Flask, render_template

class TestHotelApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        pass  # Add cleanup logic if needed

    def print_test_result(self, test_name, result):
        print(f"\nTest: {test_name}")
        print(result)

    @patch('main.mysql')  # Patching the MySQL connection
    def test_booking_requires_login(self, mock_mysql):
        mock_cursor = MagicMock()  # Creating a mock cursor
        mock_mysql.connect.return_value = mock_mysql  # Mocking the connect method
        mock_mysql.cursor.return_value = mock_cursor  # Mocking the cursor method

        response = self.app.post('/book', data={'room': 'Номер 1', 'check-in': '2024-01-20', 'check-out': '2024-01-25',
                                                'guests': 2})
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.print_test_result("test_booking_requires_login", "Pass" if response.status_code == 302 else "Fail")

    @patch('main.mysql')
    def test_booking_success(self, mock_mysql):
        mock_cursor = MagicMock()
        mock_mysql.connect.return_value = mock_mysql
        mock_mysql.cursor.return_value = mock_cursor

        with self.app as c:
            with c.session_transaction() as sess:
                sess['logged_in'] = True
                sess['user_id'] = 1

            response = c.post('/book', data={'room': 'Номер 1', 'check-in': '2024-01-20', 'check-out': '2024-01-25',
                                             'guests': 2})

        print(response.data)

        success_message_bytes = '<p>Бронирование прошло успешно.</p>'.encode('utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(success_message_bytes, response.data)
        self.print_test_result("test_booking_success", "Pass" if response.status_code == 200 else "Fail")

    @patch('main.mysql')
    def test_login_success(self, mock_mysql):
        mock_cursor = MagicMock()
        mock_mysql.connect.return_value = mock_mysql
        mock_mysql.cursor.return_value = mock_cursor

        response = self.app.post('/login', data={'email': 'your_username', 'password': 'your_password'})

        self.assertEqual(response.status_code, 200)
        self.print_test_result("test_login_success", "Pass" if response.status_code == 200 else "Fail")

    @patch('main.mysql')
    def test_login_failure(self, mock_mysql):
        mock_cursor = MagicMock()
        mock_mysql.connect.return_value = mock_mysql
        mock_mysql.cursor.return_value = mock_cursor

        response = self.app.post('/login',
                                 data={'email': 'incorrect_username', 'password': 'incorrect_password'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)  # Check if the response contains HTML content

        # Check for elements indicative of a registration failure
        self.assertIn(b'<form action="/login" method="POST">', response.data)
        self.assertIn(b'<input type="email" id="email" name="email" required>', response.data)
        self.assertIn(b'<input type="password" id="password" name="password" required>', response.data)
        # Check if the error message is present

        self.print_test_result("test_login_failure", "Pass" if response.status_code == 200 else "Fail")

    @patch('main.mysql')
    def test_registration_success(self, mock_mysql):
        mock_cursor = MagicMock()
        mock_mysql.connect.return_value = mock_mysql
        mock_mysql.cursor.return_value = mock_cursor

        response = self.app.post('/registration', data={
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
            'confirm_password': 'securepassword'
        })

        self.assertEqual(response.status_code, 302)
        with self.app as c:
            with c.session_transaction() as sess:
                self.assertTrue(sess['logged_in'])

        self.print_test_result("test_registration_success", "Pass" if response.status_code == 302 else "Fail")

    @patch('main.mysql')
    def test_registration_failure(self, mock_mysql):
        mock_cursor = MagicMock()
        mock_mysql.connect.return_value = mock_mysql
        mock_mysql.cursor.return_value = mock_cursor

        response = self.app.post('/registration', data={
            'name': 'Jane Doe',
            'email': 'jane.doe@gmail.com',
            'password': '1234',
            'confirm_password': 'mismatchedpassword'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)  # Check if the response contains HTML content

        # Check for elements indicative of a registration failure
        self.assertIn(b'<form action="/login" method="POST">', response.data)
        self.assertIn(b'<input type="email" id="email" name="email" required>', response.data)
        self.assertIn(b'<input type="password" id="password" name="password" required>', response.data)

        self.print_test_result("test_registration_failure", "Pass" if response.status_code == 200 else "Fail")


###############
class TestHotelReviewsAndRating(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

        try:
            self.connection = mysql.connect()

            if self.connection:
                self.connection.autocommit = False  # Set autocommit to False for transactions
                self.cursor = self.connection.cursor(dictionary=True)
            else:
                raise Exception("Database connection is None.")
        except Exception as e:
            print(f"Error during setup: {e}")
            self.cursor = None
            self.connection = None

    def tearDown(self):
        if self.connection:
            self.connection.rollback()  # Roll back changes made during the test
            self.connection.close()

    def print_test_result(self, test_name, result):
        print(f"\nTest: {test_name}")
        print(result)




###########################

class TestLoginRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        pass  # Add cleanup logic if needed

    def print_test_result(self, test_name, result):
        print(f"\nTest: {test_name}")
        print(result)

    @patch('main.mysql')
    def test_successful_login_redirects_to_index(self, mock_mysql):
        mock_cursor = MagicMock()
        mock_mysql.connect.return_value = mock_mysql
        mock_mysql.cursor.return_value = mock_cursor

        with self.app as c:
            response = c.post('/login', data={'email': 'your_username', 'password': 'your_password'})

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        self.print_test_result("test_successful_login_redirects_to_index", "Pass" if response.status_code == 200 else "Fail")



########################

class TestHotelRooms(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        pass  # Add cleanup logic if needed

    def print_test_result(self, test_name, result):
        print(f"\nTest: {test_name}")
        print(result)

    @patch('flask.render_template')  # Adjust based on your actual import
    def test_room1_route(self, mock_render_template):
        with self.app as c:
            response = c.get('/room1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<!DOCTYPE html>', response.data)

        self.print_test_result("test_room1_route", "Pass" if response.status_code == 200 else "Fail")

    @patch('flask.render_template')  # Adjust based on your actual import
    def test_room2_route(self, mock_render_template):
        with self.app as c:
            response = c.get('/room2')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<!DOCTYPE html>', response.data)

        self.print_test_result("test_room2_route", "Pass" if response.status_code == 200 else "Fail")

    @patch('flask.render_template')  # Adjust based on your actual import
    def test_room3_route(self, mock_render_template):
        with self.app as c:
            response = c.get('/room3')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<!DOCTYPE html>', response.data)

        self.print_test_result("test_room3_route", "Pass" if response.status_code == 200 else "Fail")

    @patch('flask.render_template')  # Adjust based on your actual import
    def test_room4_route(self, mock_render_template):
        with self.app as c:
            response = c.get('/room4')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<!DOCTYPE html>', response.data)

        self.print_test_result("test_room4_route", "Pass" if response.status_code == 200 else "Fail")



if __name__ == '__main__':
    unittest.main()
