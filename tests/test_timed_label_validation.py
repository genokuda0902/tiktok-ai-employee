import unittest
from src.timed_label_validation import Cue, validate_cues, ffmpeg_enable

class TestTimedLabels(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_cues([Cue(3,6,"目的"),Cue(12,15,"条件")],23.033))
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            validate_cues([Cue(3,6,"a"),Cue(5,7,"b")],23)
    def test_blank_rejected(self):
        with self.assertRaises(ValueError):
            validate_cues([Cue(3,6," ")],23)
    def test_bounds_rejected(self):
        with self.assertRaises(ValueError):
            validate_cues([Cue(22,24,"a")],23)
    def test_enable(self):
        self.assertEqual(ffmpeg_enable(Cue(3,6,"a")),"between(t,3,6)")

if __name__ == "__main__":
    unittest.main()
