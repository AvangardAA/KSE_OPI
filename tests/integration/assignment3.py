import unittest
from unittest.mock import patch
import asyncio

from functions.funcs import total_time_avg, total_time_user

class TestIntegration(unittest.TestCase):
    @patch('functions.funcs.fetch')
    def test_get_users_historical_data_wrong_fetch(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 1, "data": [{"userId": "user", "lastSeenDate": "2023-10-19T10:47:29.2227007+00:00"}]}
            blank_user = "user"
            result = await total_time_user(blank_user)

            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['totalTime'])>0)

        asyncio.run(async_test())

    @patch('functions.funcs.fetch')
    def test_get_users_historical_data_valid_fetch(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 1, "data": [{"userId": "user", "lastSeenDate": "2023-10-19T10:47:29.2227007+00:00"}]}
            blank_user = "user"
            result = await total_time_user(blank_user)

            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['totalTime'])>0)

        asyncio.run(async_test())

    @patch('functions.funcs.fetch')
    def test_get_user_historical_data_wrong_fetch(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 1, "data": [{"userId": "user", "lastSeenDate": "2023-10-19T10:47:29.2227007+00:00"}]}
            blank_user = "user"
            result = await total_time_user(blank_user)

            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['totalTime'])>0)

        asyncio.run(async_test())

    @patch('functions.utils.check_dates_correspond')
    def test_predict_users_check_dont_correspond(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 1, "data": [{"userId": "user", "lastSeenDate": "2023-10-19T10:47:29.2227007+00:00"}]}
            blank_user = "user"
            result = await total_time_user(blank_user)

            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['totalTime'])>0)

        asyncio.run(async_test())


    def test_predict_users_transform_invalid(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 1, "data": [{"userId": "user", "lastSeenDate": "2023-10-19T10:47:29.2227007+00:00"}]}
            blank_user = "user"
            result = await total_time_user(blank_user)

            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['totalTime'])>0)

        asyncio.run(async_test())

    def test_predict_user_check_correspond_invalid(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 1, "data": [{"userId": "user", "lastSeenDate": "2023-10-19T10:47:29.2227007+00:00"}]}
            blank_user = "user"
            result = await total_time_user(blank_user)

            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['totalTime'])>0)

        asyncio.run(async_test())

    def test_predict_user_transform_invalid(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = {"total": 1, "data": [{"userId": "user", "lastSeenDate": "2023-10-19T10:47:29.2227007+00:00"}]}
            blank_user = "user"
            result = await total_time_user(blank_user)

            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['totalTime'])>0)

        asyncio.run(async_test())

if __name__ == '__main__':
    unittest.main()