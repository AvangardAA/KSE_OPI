import asyncio
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

    async def test_get_reports_307_then_200_then_fail(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://127.0.0.1:8000/api/report?report_name=dummy1&ffrom=2023-19-10-07:00&to=2023-23-10-07:00&ver=1")

            if response.status_code == 307:
                location = response.headers.get("Location")
                response = await client.get(location)

            data = response.text

            if response.status_code != 200:
                self.assertEqual(response.status_code, 404)
            else:
                try:
                    parsed_data = json.loads(data)
                    self.assertEqual(parsed_data, {"err": "invalid report name"})
                except json.JSONDecodeError:
                    self.fail("Response is not valid JSON")

    async def test_get_reports_200(self):
        async with httpx.AsyncClient() as client:

            response = await client.get(
                "http://127.0.0.1:8000/api/report?report_name=dummy1&ffrom=2023-19-10-07:00&to=2023-23-10-07:00&ver=1")

            if response.status_code == 307:
                location = response.headers.get("Location")
                response = await client.get(location)

            data = response.text

            if response.status_code != 200:
                self.assertEqual(response.status_code, 404)
            else:
                try:
                    parsed_data = json.loads(data)
                    self.assertIsInstance(parsed_data, dict)
                    self.assertTrue(len(parsed_data)==1)
                except json.JSONDecodeError:
                    self.fail("Response is not valid JSON")

    async def test_get_reports_V2_200(self):
        async with httpx.AsyncClient() as client:
            async with httpx.AsyncClient() as client:

                response = await client.get(
                    "http://127.0.0.1:8000/api/report?report_name=dummy1&ffrom=2023-19-10-07:00&to=2023-23-10-07:00&ver=2")

                if response.status_code == 307:
                    location = response.headers.get("Location")
                    response = await client.get(location)

                data = response.text

                if response.status_code != 200:
                    self.assertEqual(response.status_code, 404)
                else:
                    try:
                        parsed_data = json.loads(data)
                        self.assertIsInstance(parsed_data, dict)
                        self.assertTrue(len(parsed_data) == 1)
                    except json.JSONDecodeError:
                        self.fail("Response is not valid JSON")

    def test_start_get200_fail(self):
        asyncio.run(self.test_get_reports_307_then_200_then_fail())

    def test_start_get200(self):
        asyncio.run(self.test_get_reports_200())

    def test_start_get200V2(self):
        asyncio.run(self.test_get_reports_V2_200())

if __name__ == '__main__':
    unittest.main()
