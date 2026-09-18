import unittest
from src.analytics_improvement import parse, analyze

BASE = {'account_id':'a','video_id':'v1','video_url':'https://www.tiktok.com/@example/video/123','published_at':'2026-09-18T12:00:00+09:00','genre':'tips','hook_type':'question','views':'100','likes':'2','comments':'1','shares':'0'}

class AnalyticsTests(unittest.TestCase):
    def test_aggregation(self):
        result = analyze([parse(BASE)])
        self.assertEqual(result['a']['by_genre'][0]['total_views'], 100)
        self.assertEqual(result['a']['improvement']['status'], 'insufficient_evidence')

    def test_missing_metrics_not_fabricated(self):
        row = dict(BASE, views='', average_watch_seconds='', completion_rate='')
        result = analyze([parse(row)])
        self.assertIsNone(result['a']['by_genre'][0]['total_views'])
        self.assertEqual(result['a']['measured_videos'], 0)

    def test_account_separation(self):
        other = dict(BASE, account_id='b', views='9')
        result = analyze([parse(BASE), parse(other)])
        self.assertEqual(result['a']['by_genre'][0]['total_views'], 100)
        self.assertEqual(result['b']['by_genre'][0]['total_views'], 9)

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            analyze([parse(BASE), parse(BASE)])

    def test_invalid_completion_rejected(self):
        with self.assertRaises(ValueError):
            parse(dict(BASE, completion_rate='80'))

if __name__ == '__main__':
    unittest.main()
