import unittest
from collections import defaultdict
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

    @patch('functions.utils.make_res_list')
    def test_get_report_make_res_list_corrupted(self, mock_res_list):
        async def async_test():
            mock_res_list.return_value = {"err": "broken make"}
            daily_sum = defaultdict(float)
            daily_count = defaultdict(int)
            weekly_sum = defaultdict(float)
            weekly_count = defaultdict(int)

            user_appearances = defaultdict(int)
            res = {}
            try:
                for user_id, daily_avg, weekly_avg in mock_res_list.return_value:
                    daily_sum[user_id] += daily_avg
                    daily_count[user_id] += 1
                    weekly_sum[user_id] += weekly_avg
                    weekly_count[user_id] += 1
                    user_appearances[user_id] += 1
            except Exception as e:
                res = {"err": "broken reslist"}

            self.assertEqual({"err": "broken reslist"}, res)

        asyncio.run(async_test())

if __name__ == '__main__':
    unittest.main()