import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from algo import app


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_gdpr_integration(self):
        with patch('algo.gdprf') as mock_gdprf:
            mock_gdprf.return_value = {'msg': 'added successfully'}

            response = self.client.post("/api/user/forget?userId=test123")
            self.assertEqual(response.json(), {'msg': 'added successfully'})

    def test_get_users_historical_data_integration(self):
        with patch('algo.hist_data') as mock_hist_data:
            mock_hist_data.return_value = {'usersOnline': 0, 'users': []}

            response = self.client.get("/api/stats/users?date=2023-10-17")

            self.assertEqual(response.json(), {'usersOnline': 0, 'users': []})
    def test_get_user_historical_data_integration(self):
        with patch('algo.user_hist_data') as mock_user_hist_data:
            mock_user_hist_data.return_value = {'wasUserOnline': False, 'nearestOnlineTime': None}
            response = self.client.get("/api/stats/user?date=2023-10-17&userId=test123")
            self.assertEqual(response.json(), {'wasUserOnline': False, 'nearestOnlineTime': None})

    def test_predict_users_online_integration(self):
        with patch('algo.predict_users') as mock_predict_users:
            mock_predict_users.return_value = {'OnlineUsers': 0}
            response = self.client.get("/api/predictions/users?date=2023-10-17")
            self.assertEqual(response.json(), {'OnlineUsers': 0})

    def test_predict_user_online_integration(self):
        with patch('algo.predict_user') as mock_predict_user:
            mock_predict_user.return_value = {'willBeOnline': False, 'onlineChance': '0.00'}
            response = self.client.get("/api/predictions/user?date=2023-10-17&tolerance=0.1&userId=test123")
            self.assertEqual(response.json(), {'willBeOnline': False, 'onlineChance': '0.00'})

    def test_total_time_integration(self):
        with patch('algo.total_time_user') as mock_total_time_user:
            mock_total_time_user.return_value = {'totalTime': []}
            response = self.client.get("/api/stats/user/total?userId=test123,test456")
            self.assertEqual(response.json(), {'totalTime': []})

    def test_total_time_avg_integration(self):
        with patch('algo.total_time_avg') as mock_total_time_avg:
            mock_total_time_avg.return_value = {'dailyAverage': [], 'weeklyAverage': []}
            response = self.client.get("/api/stats/user/total/avg?userId=test123,test456")
            self.assertEqual(response.json(), {'dailyAverage': [], 'weeklyAverage': []})

    def test_post_report_integration(self):
        with patch('algo.total_time_user') as mock_total_time_user, patch('algo.total_time_avg') as mock_total_time_avg:
            mock_total_time_user.return_value = {'totalTime': []}
            mock_total_time_avg.return_value = {'dailyAverage': [], 'weeklyAverage': []}
            response = self.client.post("/api/report/?report_name=test_report", json={"users": ["test123", "test456"], "metrics": ["dailyAverage","weeklyAverage"]})
            self.assertEqual(response.status_code, 200)