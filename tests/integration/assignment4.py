import unittest
from unittest.mock import patch
import asyncio

from functions.funcs import total_time_avg, total_time_user

class TestIntegration(unittest.TestCase):
    @patch('functions.funcs.fetch')
    def test_total_time_user_not_empty(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 1, "data": [{"userId": "user", "lastSeenDate": "2023-10-19T10:47:29.2227007+00:00"}]}
            blank_user = "user"
            result = await total_time_user(blank_user)

            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['totalTime'])>0)

        asyncio.run(async_test())

    @patch('functions.funcs.fetch')
    def test_total_time_user_empty(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 0, "data": []}
            blank_user = "user"
            result = await total_time_user(blank_user)

            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['totalTime'])==0)

        asyncio.run(async_test())

    @patch('functions.funcs.fetch')
    def test_total_time_user_invalid_last_seen(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 1, "data": [{"userId": "user","lastSeenDate": None}]}
            blank_user = "user"
            result = await total_time_user(blank_user)
            self.assertIsInstance(result, dict)
            self.assertTrue(result['totalTime']==[0])

        asyncio.run(async_test())
    @patch('functions.funcs.total_time_user')
    def test_total_time_avg_integration_not_empty_response(self, mock_total_time):
        async def async_test():
            user_id = ["user1"]
            mock_total_time.return_value = {"totalTime": [100000]}

            result = await total_time_avg(user_id)
            self.assertIsInstance(result, dict)
            self.assertIn("dailyAverage", result)
            self.assertIn("weeklyAverage", result)
            self.assertTrue(len(result['dailyAverage']) == len(mock_total_time.return_value['totalTime']))
            self.assertTrue(len(result['weeklyAverage']) == len(mock_total_time.return_value['totalTime']))
        asyncio.run(async_test())

    @patch('functions.funcs.total_time_user')
    def test_total_time_avg_integration_empty_response(self, mock_total_time):
        async def async_test():
            user_id = ["user1"]
            mock_total_time.return_value = {"totalTime": []}

            result = await total_time_avg(user_id)
            self.assertIsInstance(result, dict)
            self.assertIn("dailyAverage", result)
            self.assertIn("weeklyAverage", result)
            self.assertTrue(len(result['dailyAverage']) == len(mock_total_time.return_value['totalTime']) == 0)
            self.assertTrue(len(result['weeklyAverage']) == len(mock_total_time.return_value['totalTime']) == 0)

        asyncio.run(async_test())

if __name__ == '__main__':
    unittest.main()