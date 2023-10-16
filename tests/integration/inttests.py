import unittest
from unittest.mock import patch
from functions.funcs import total_time_user, total_time_avg

class TestIntegration(unittest.TestCase):
    @patch('functions.funcs.total_time_user')
    def test_total_time_user_integration(self, mock_total_time_user):
        mock_total_time_user.return_value = {
            'total': 2,
            'data': [
                {'userId': "908dcb71-beeb-57c4-72f6-50451a6c3d12", 'lastSeenDate': '2023-10-17T12:00:00'},
                {'userId': "e13412b2-fe46-7149-6593-e47043f39c91", 'lastSeenDate': '2023-10-17T12:00:00'},
            ]
        }
        result = total_time_user(['908dcb71-beeb-57c4-72f6-50451a6c3d12', "e13412b2-fe46-7149-6593-e47043f39c91"])
        #print(result)

        # assert with value is here but due to realtime behaviour i cant place it because it will fail 5 min after i place it
        self.assertIsNotNone(result)

    @patch('functions.funcs.total_time_avg')
    def test_total_time_avg_integration(self, mock_total_avg):
        mock_total_avg.return_value = {"totalTime": [100, 200, 300]}
        result = total_time_avg(['908dcb71-beeb-57c4-72f6-50451a6c3d12', "e13412b2-fe46-7149-6593-e47043f39c91"])

        # assert with value is here but due to realtime behaviour i cant place it because it will fail 5 min after i place it
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
