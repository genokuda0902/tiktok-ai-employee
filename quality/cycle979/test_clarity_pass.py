import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from clarity_pass import (GENRE_PROFILES, ARTWORK_BOTTOM, HEIGHT, WIDTH,
                          filter_graph, validate)

class ClarityTests(unittest.TestCase):
    def test_all_genres(self):
        self.assertEqual(len(GENRE_PROFILES), 10)
        for genre, amount in GENRE_PROFILES.items():
            self.assertGreater(amount, 0)
            self.assertLessEqual(amount, 0.7)
            self.assertEqual(validate(genre, synthetic=True), amount)
    def test_unreviewed_fails_closed(self):
        with self.assertRaises(ValueError):
            validate('travel')
    def test_unknown_fails(self):
        with self.assertRaises(ValueError):
            validate('fake', synthetic=True)
    def test_ai_work_allowed(self):
        self.assertEqual(validate('ai_work'), .65)
    def test_protected_caption_area(self):
        self.assertEqual(ARTWORK_BOTTOM, 1180)
        self.assertEqual((WIDTH, HEIGHT), (1080, 1920))
    def test_filter_only_crops_upper_artwork(self):
        g = filter_graph(.65)
        self.assertIn('crop=1080:1180:0:0', g)
        self.assertIn('unsharp=5:5:0.65', g)
        self.assertIn('overlay=0:0', g)
    def test_no_mutation_or_post(self):
        g = filter_graph(.65)
        self.assertNotIn('upload', g)
        self.assertNotIn('post', g)

if __name__ == '__main__':
    unittest.main()
