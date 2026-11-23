import unittest
from quality.cycle1653_caption_safe_area import Cue, validate_cues, publication_allowed

class TestCaptionSafety(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_cues([Cue(0, 3, "開始"), Cue(3, 6, "比較")], 12))
    def test_overlap(self):
        with self.assertRaises(ValueError):
            validate_cues([Cue(0, 4, "開始"), Cue(3, 6, "比較")], 12)
    def test_safe_area(self):
        with self.assertRaises(ValueError):
            validate_cues([Cue(0, 3, "開始")], 12, top=1700, bottom=1900)
    def test_no_audio_means_no_post(self):
        self.assertFalse(publication_allowed(sync_verified=True, asset_approved=True, employee_approved=True))

if __name__ == "__main__":
    unittest.main()
