"""Smoke-test the checked-in ten-genre palette configuration."""
import json
import re
import unittest
from pathlib import Path

class QualityChecks(unittest.TestCase):
    def test_genres(self):
        path = Path(__file__).parent / 'config' / 'genres.json'
        genres = json.loads(path.read_text(encoding='utf-8'))['genres']
        self.assertEqual(len(genres), 10)
        self.assertIn('雑学・科学', genres)
        for name, value in genres.items():
            with self.subTest(genre=name):
                self.assertRegex(value, r'^#[0-9a-fA-F]{6}$')

if __name__ == '__main__':
    unittest.main()
