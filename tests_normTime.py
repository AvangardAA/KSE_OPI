from datetime import datetime, timedelta
import unittest
from algo import normalize_time_human_implementation
from algo import check_dates_correspond


class TestNormalizeTime(unittest.TestCase):

    def test_unknown(self):
        self.assertEqual(normalize_time_human_implementation(None, 'english'), '0')
        self.assertEqual(normalize_time_human_implementation(None, 'ukrainian'), '0')

    def test_unknown_format(self):
        invalid_date = "2023-09-28X23:00:11"
        self.assertEqual(normalize_time_human_implementation(invalid_date, 'english'), 'coders pain')
        self.assertEqual(normalize_time_human_implementation(invalid_date, 'ukrainian'), 'біль кодера')

    def test_now(self):
        recent_date = (datetime.utcnow() - timedelta(seconds=10)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(normalize_time_human_implementation(recent_date, 'english'), 'is online now')
        self.assertEqual(normalize_time_human_implementation(recent_date, 'ukrainian'), 'зараз онлайн')

    def test_last_min(self):
        last_minute_date = (datetime.utcnow() - timedelta(seconds=45)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(normalize_time_human_implementation(last_minute_date, 'english'), 'was online last minute')
        self.assertEqual(normalize_time_human_implementation(last_minute_date, 'ukrainian'), 'був(ла) в мережі в останню хвилину')

    def test_less_than_hour_minutes(self):
        minutes_ago_date = (datetime.utcnow() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(normalize_time_human_implementation(minutes_ago_date, 'english'), 'was online 5 minutes ago')
        self.assertEqual(normalize_time_human_implementation(minutes_ago_date, 'ukrainian'), 'був(ла) в мережі 5 хвилин тому')

    def test_user_fastapi_long_no_see(self):
        self.assertEqual(normalize_time_human_implementation("2023-10-11T20:29:33.8772757+00:00", "english", DDate="2023-9-11-20:00"), {"ts": 2493027, "status": "no"})

    def test_user_fastapi_seen(self):
        was = False
        nearest = None
        res = normalize_time_human_implementation("2023-10-11T20:29:33.8772757+00:00", "english", DDate="2023-11-10-23:00")
        if res["status"] == "yes":
            was = True
        else:
            nearest = int(res["ts"])
            if nearest is not None:
                if nearest < res["ts"]:
                    nearest = res["ts"]

        if was:
            nearest = None
        self.assertEqual({"wasUserOnline": was, "nearestOnlineTime": nearest}, {"wasUserOnline": True, "nearestOnlineTime": None})

    def test_date_checker(self):
        self.assertEqual(check_dates_correspond("2025-27-09-20:00", "2025-13-09-20:00"), True)
        self.assertEqual(check_dates_correspond("2025-27-09-20:00", "2025-14-09-20:00"), False)