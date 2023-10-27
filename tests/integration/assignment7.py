import unittest
from unittest.mock import patch
import asyncio

from functions.funcs import get_reports
from functions.utils import transform_metrics_list


class TestIntegration(unittest.TestCase):
    @patch('functions.funcs.get_reports')
    def test_get_reports_metricsV2_OK(self, mock_get_reports):
        async def async_test():
            mock_get_reports.return_value = [{"userId": "e13412b2-fe46-7149-6593-e47043f39c91","metrics": [{"dailyAverage": 29418.0},{"weeklyAverage": 205926.0},{"total": 88254.0},{"min": 0.0},{"max": 83874.0}]},{"userId": "e9de6dd1-84e5-9833-59de-8c51008de6a0","metrics": [{"dailyAverage": 17515.333333333332},{"weeklyAverage": 122607.33333333333},{"total": 52546.0},{"min": 0.0},{"max": 83874.0}]}]
            res = transform_metrics_list(mock_get_reports.return_value)

            self.assertIsInstance(res, dict)
            self.assertTrue(len(res['users'])==2)

        asyncio.run(async_test())

    @patch('functions.funcs.get_reports')
    def test_get_reports_metricsV2_NOT_OK(self, mock_get_reports):
        async def async_test():
            mock_get_reports.return_value = [{}]
            try:
                res = transform_metrics_list(mock_get_reports.return_value)
            except KeyError as e:
                self.assertEqual(str(e), "'userId'")
            else:
                self.fail("KeyError was not raised")

        asyncio.run(async_test())

if __name__ == '__main__':
    unittest.main()