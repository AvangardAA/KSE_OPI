import unittest

from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json

from algo import app

client = TestClient(app)
class TestAPI(unittest.TestCase):
    @patch('requests.post')
    def test_gdpr(self, mock_post):
        expected_response = {'msg': 'added successfully'}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        mock_post.return_value = mock_response

        response = client.post("/api/user/forget?userId=test123")
        #print(response.json())
        assert response.json() == expected_response
    @patch('requests.get')
    async def test_get_users_historical_data(self, mock_get):
        expected_response_should_contain = "usersOnline"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response_should_contain

        mock_get.return_value = mock_response

        response = await client.get("/api/stats/users?date=2023-10-17")
        assert (expected_response_should_contain in response.json())
    @patch('requests.get')
    async def test_get_user_historical_data(self, mock_get):
        expected_response = {"wasUserOnline": False, "nearestOnlineTime": None}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        mock_get.return_value = mock_response

        response = await client.get("/api/stats/user?date=2023-10-17&userId=test123")

        assert response.json() == expected_response
    @patch('requests.get')
    async def test_predict_users_online(self, mock_get):
        expected_response_should_contain = "OnlineUsers"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response_should_contain

        mock_get.return_value = mock_response

        response = await client.get("/api/predictions/users?date=2023-10-17")

        assert (expected_response_should_contain in response.json())
    @patch('requests.get')
    async def test_predict_user_online(mock_get):
        expected_response = {"willBeOnline": False, "onlineChance": "0.00"}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        mock_get.return_value = mock_response

        response = await client.get("/api/predictions/user?date=2023-10-17&tolerance=0.1&userId=test123")

        assert response.json() == expected_response
    @patch('requests.get')
    async def test_totalTime(self, mock_get):
        expected_response = {"totalTime": []}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        mock_get.return_value = mock_response

        response = await client.get("/api/stats/user/total?userId=test123,test456")
        assert response.json() == expected_response
    @patch('requests.get')
    async def test_totalTimeAvg(self, mock_get):
        expected_response = {"dailyAverage": [], "weeklyAverage": []}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        mock_get.return_value = mock_response

        response = await client.get("/api/stats/user/total/avg?userId=test123,test456")

        assert response.json() == expected_response
    @patch('requests.post')
    @patch('requests.get')
    async def test_post_report(self, mock_post, mock_get):
        expected_post_response = {}

        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = expected_post_response

        mock_post.return_value = mock_post_response

        expected_get_response = {"dailyAverage": [], "weeklyAverage": []}

        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = expected_get_response

        mock_get.side_effect = [mock_get_response, mock_get_response]

        response = await client.post("/api/report/?report_name=test_report", json={"users": ["test123", "test456"],
                                                                             "metrics": ["dailyAverage",
                                                                                         "weeklyAverage"]})
        assert response.json() == expected_post_response
