from datetime import datetime, timedelta
import unittest
from algo import normalize_time
class TestNormalizeTime(unittest.TestCase):

    def test_unknown(self):
        self.assertEqual(normalize_time(None, 'english'), '0')
        self.assertEqual(normalize_time(None, 'ukrainian'), '0')

    def test_unknown_format(self):
        invalid_date = "2023-09-28X23:00:11"
        self.assertEqual(normalize_time(invalid_date, 'english'), 'coders pain')
        self.assertEqual(normalize_time(invalid_date, 'ukrainian'), 'біль кодера')

    def test_now(self):
        recent_date = (datetime.utcnow() - timedelta(seconds=10)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(normalize_time(recent_date, 'english'), 'is online now')
        self.assertEqual(normalize_time(recent_date, 'ukrainian'), 'зараз онлайн')

    def test_last_min(self):
        last_minute_date = (datetime.utcnow() - timedelta(seconds=45)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(normalize_time(last_minute_date, 'english'), 'was online last minute')
        self.assertEqual(normalize_time(last_minute_date, 'ukrainian'), 'був(ла) в мережі в останню хвилину')

    def test_less_than_hour_minutes(self):
        minutes_ago_date = (datetime.utcnow() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(normalize_time(minutes_ago_date, 'english'), 'was online 5 minutes ago')
        self.assertEqual(normalize_time(minutes_ago_date, 'ukrainian'), 'був(ла) в мережі 5 хвилин тому')
