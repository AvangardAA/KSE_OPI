import unittest
from collections import defaultdict
from unittest.mock import patch
import asyncio

from functions.funcs import helper_function_exam, get_uuser_list_exam

class TestIntegration(unittest.TestCase):

    @patch('functions.funcs.fetch')
    def test_helper_func_fetch_empty(self, mock_fetch):
        async def async_test():
            mock_fetch.return_value = []
            res = await helper_function_exam()

            self.assertIsInstance(res, dict)
            self.assertTrue(res == {"msg":"error"})

        asyncio.run(async_test())

    @patch('functions.funcs.helper_function_exam')
    def test_exam_return_endpoint(self, mock_helper):
        async def async_test():
            mock_helper.return_value = "failure"

            res = await get_uuser_list_exam()
            self.assertIsInstance(res, dict)
            self.assertTrue(res == {"err": "some error"})

        asyncio.run(async_test())


if __name__ == '__main__':
    unittest.main()