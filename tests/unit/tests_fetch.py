import unittest
from unittest.mock import patch, Mock
import requests

from functions.funcs import fetch


class TestFetchFunction(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_200_empty(self, mockres):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mockres.return_value = mock_response
        res = fetch(0)
        self.assertEqual(res, {"data": []})
    @patch('requests.get')
    def test_fetch_500(self, mockres):
        mock_response = Mock()
        mock_response.status_code = 500
        mockres.return_value = mock_response
        res = fetch(0)
        self.assertEqual(res, [])
    @patch('requests.get')
    def test_fetch_conerror(self, mockres):
        mockres.side_effect = requests.exceptions.RequestException("http connection error")
        res = fetch(0)
        self.assertEqual(res, [])
    @patch('requests.get')
    def test_fetch_timeout(self, mockres):
        mockres.side_effect = requests.exceptions.RequestException("timeout")
        res = fetch(0)
        self.assertEqual(res, [])
    @patch('requests.get')
    def test_fetch_formaterror(self, mockres):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "0"
        mockres.return_value = mock_response
        res = fetch(0)
        self.assertEqual(res, [])
