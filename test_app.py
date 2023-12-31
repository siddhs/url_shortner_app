import unittest
import json
from unittest.mock import patch, MagicMock
from app import app
import datetime

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.get_db_connection')
    def test_urlshortner_post_api(self, mock_get_db_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        response = self.app.post('/', data={
            'url': 'https://example.com',
            'expiry': '2023-12-31'
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('shortened_url', data)

    @patch('app.get_db_connection')
    def test_urlshortner_post_api_if_empty_url_is_passed(self, mock_get_db_connection):
        response = self.app.post('/', data={
            'url': '',
            'expiry': ''
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Empty URL!")

    @patch('app.get_db_connection')
    def test_urlshortner_post_api_if_invalid_url_is_passed(self, mock_get_db_connection):
        response = self.app.post('/', data={
            'url': 'abcdef',
            'expiry': ''
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], "Invalid URL!!")
    
    @patch('app.get_db_connection')    
    def test_homepage_api(self, mock_get_db_connection):
        response = self.app.get('/')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)

    @patch('app.get_db_connection')
    def test_stats_api(self, mock_get_db_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Mock the execute method to return mock URL data
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{"clicks": 1,
                                              "clicks_last_24h": 1,
                                              "clicks_past_week": 1,
                                              "created": "2023-08-10 14:14:30",
                                              "expiry": "2033-08-07 07:14:30.718545",
                                              "id": "aXgx",
                                              "original_url": "https://example.com",
                                              "short_url": "http://127.0.0.1:5000/ZO0g"}]

        response = self.app.get('/stats')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('urls', data)

    @patch('app.get_db_connection')
    def test_delete_url_api(self, mock_get_db_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Mock the execute method to return mock URL data
        mock_cursor = MagicMock()
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'short_url': 'http://127.0.0.1:5000/ZO0g'}

        # Assuming you have an existing URL with ID 'ZO0g'
        response = self.app.delete('/delete/ZO0g')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()