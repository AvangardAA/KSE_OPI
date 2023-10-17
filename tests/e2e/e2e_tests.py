import unittest
import json
import http.client

class TestE2E(unittest.TestCase):
    def setUp(self):
        self.conn = http.client.HTTPConnection("127.0.0.1:8000")  # Update with your server's host and port

    def tearDown(self):
        self.conn.close()

    def test_total_time_endpoint(self):
        self.conn.request("GET", "/api/stats/user/total?userId=1111")
        response = self.conn.getresponse()
        data = response.read().decode()
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(data), {"totalTime": []})

        self.conn.request("GET", "/api/stats/user/total?userId=e13412b2-fe46-7149-6593-e47043f39c91")
        response = self.conn.getresponse()
        data = response.read().decode()
        self.assertEqual(response.status, 200)
        self.assertTrue(len(json.loads(data)["totalTime"]) > 0)

    def test_total_time_avg_endpoint(self):
        self.conn.request("GET", "/api/stats/user/total/avg?userId=1111")
        response = self.conn.getresponse()
        data = response.read().decode()
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(data), {"dailyAverage": [], 'weeklyAverage': []})

        self.conn.request("GET", "/api/stats/user/total/avg?userId=e13412b2-fe46-7149-6593-e47043f39c91")
        response = self.conn.getresponse()
        data = response.read().decode()
        self.assertEqual(response.status, 200)
        self.assertTrue("dailyAverage" in json.loads(data))
        self.assertTrue("weeklyAverage" in json.loads(data))

if __name__ == '__main__':
    unittest.main()
