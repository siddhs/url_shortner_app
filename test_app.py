import unittest
import json
from unittest.mock import patch, MagicMock
from app import app

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

if __name__ == '__main__':
    unittest.main()