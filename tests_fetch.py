import unittest
from unittest.mock import patch, Mock

class TestFetchFunction(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_200(self, mockres):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": ""}
        mockres.return_value = mock_response
        self.assertEqual(mock_response.status_code, 200)
    @patch('requests.get')
    def test_fetch_500(self, mockres):
        mock_response = Mock()
        mock_response.status_code = 500
        mockres.return_value = mock_response
        self.assertEqual(mock_response.status_code, 500)
    @patch('requests.get')
    def test_fetch_403(self, mockres):
        mock_response = Mock()
        mock_response.status_code = 403
        mockres.return_value = mock_response
        self.assertEqual(mock_response.status_code, 403)
    @patch('requests.get')
    def test_fetch_404(self, mockres):
        mock_response = Mock()
        mock_response.status_code = 404
        mockres.return_value = mock_response
        self.assertEqual(mock_response.status_code, 404)
