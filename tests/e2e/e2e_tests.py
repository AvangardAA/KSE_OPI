import unittest
import json
import http.client

import httpx


class TestE2E(unittest.TestCase):
    def setUp(self):
        self.conn = http.client.HTTPConnection("127.0.0.1:8000")

    def tearDown(self):
        self.conn.close()

    def test_total_time_endpoint(self):
        self.conn.request("GET", "/api/stats/user/total?userId=1111")
        response = self.conn.getresponse()
        data = response.read().decode()
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(data), {"totalTime": []})

        self.conn.request("GET", "/api/stats/user/total?userId=2fba2529-c166-8574-2da2-eac544d82634")
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

        self.conn.request("GET", "/api/stats/user/total/avg?userId=2fba2529-c166-8574-2da2-eac544d82634")
        response = self.conn.getresponse()
        data = response.read().decode()
        self.assertEqual(response.status, 200)
        self.assertTrue("dailyAverage" in json.loads(data))
        self.assertTrue("weeklyAverage" in json.loads(data))

    async def test_get_reports_307_then_200(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://127.0.0.1/api/report?report_name=dummy1&ffrom=2023-19-10-07:00&to=2023-23-10-07:00")

            if response.status_code == 307:
                location = response.headers.get("Location")
                response = await client.get(location)

            data = response.text

            if response.status_code != 200:
                # Handle non-200 responses, e.g., report not found
                self.assertEqual(response.status_code, 404)  # Update the status code as needed
            else:
                try:
                    parsed_data = json.loads(data)
                    self.assertEqual(parsed_data, {"err": "invalid report name"})
                except json.JSONDecodeError:
                    self.fail("Response is not valid JSON")

    async def test_get_reports_200(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://127.0.0.1/api/report?report_name=dummy&ffrom=2023-19-10-07:00&to=2023-23-10-07:00")

            data = response.text

            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(data) == 2)

if __name__ == '__main__':
    unittest.main()
