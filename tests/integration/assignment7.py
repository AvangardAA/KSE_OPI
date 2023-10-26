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

if __name__ == '__main__':
    unittest.main()