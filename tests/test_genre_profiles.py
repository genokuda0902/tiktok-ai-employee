import json
import tempfile
import unittest
from pathlib import Path
from src.genre_profiles import load_profiles, metric_value, plan_for_genre, PROFILE_PATH


class GenreProfilesTest(unittest.TestCase):
    def test_ten_profiles_load(self):
        self.assertEqual(len(load_profiles()['genres']), 10)

    def test_distinct_genre_rules(self):
        self.assertNotEqual(plan_for_genre('ai_productivity')['visual'], plan_for_genre('cooking')['visual'])

    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError):
            plan_for_genre('unknown')

    def test_missing_metric_not_zero(self):
        self.assertIsNone(metric_value({}, 'completion_rate'))
        self.assertIsNone(metric_value({'completion_rate': -1}, 'completion_rate'))
        self.assertEqual(metric_value({'completion_rate': 0}, 'completion_rate'), 0)

    def test_policy_cannot_disable_manual_posting(self):
        config = json.loads(PROFILE_PATH.read_text(encoding='utf-8'))
        config['default_policy']['publish_mode'] = 'automatic'
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'config.json'
            path.write_text(json.dumps(config), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_profiles(path)


if __name__ == '__main__':
    unittest.main()
