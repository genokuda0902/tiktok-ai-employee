"""Unit tests for cycle682 Japanese speech and review gate."""
import unittest
from voice_contract import GENRES, make_cues, can_publish

class TestVoiceContract(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(set(GENRES)), 10)
    def test_cues_use_measured_lengths(self):
        for genre in GENRES:
            cues = make_cues(["短い説明"] * 10, [1.25] * 10, genre)
            self.assertEqual(len(cues), 10)
            self.assertEqual(cues[1].start, 2.0)
            self.assertEqual(cues[9].end, 19.25)
    def test_rejects_overflow(self):
        with self.assertRaises(ValueError):
            make_cues(["短い説明"] * 10, [2.01] * 10)
    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            make_cues([""] * 10, [1.0] * 10)
    def test_publish_requires_all_four_gates(self):
        self.assertFalse(can_publish(False, True, True, True))
        self.assertFalse(can_publish(True, True, True, False))
        self.assertTrue(can_publish(True, True, True, True))

if __name__ == "__main__":
    unittest.main()
