import unittest
from unittest.mock import patch
import asyncio

from functions.funcs import total_time_avg, total_time_user

class TestIntegration(unittest.TestCase):
    @patch('functions.funcs.total_time_user')
    def test_post_metrics_corrupted_total_time(self, mock_total_time):
        async def async_test():
            mock_total_time.return_value = {}
            try:
                res = await total_time_avg(mock_total_time.return_value)
            except KeyError as e:
                self.assertEqual(str(e), "'totalTime'")
            else:
                self.fail("KeyError was not raised")

        asyncio.run(async_test())

if __name__ == '__main__':
    unittest.main()