"""Cycle605 original audio unit checks (no external media required)."""
import unittest
import numpy as np
from quality_cycles.cycle605.sound_core import GENRES, CUES, SAMPLE_RATE, soundtrack

class SoundtrackTests(unittest.TestCase):
    def test_all_genres(self):
        for genre in GENRES:
            a = soundtrack(2.5, genre)
            self.assertEqual(a.shape, (round(2.5*SAMPLE_RATE), 2))
            self.assertTrue(np.isfinite(a).all())
            self.assertLess(float(np.max(np.abs(a))), 0.9)
    def test_deterministic(self):
        self.assertTrue(np.array_equal(soundtrack(2.5), soundtrack(2.5)))
    def test_cues(self):
        self.assertEqual(len(CUES), 10)
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):
            soundtrack(2.5, "unknown")

if __name__ == "__main__":
    unittest.main()
