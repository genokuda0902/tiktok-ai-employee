import unittest
from src.caption_timeline import validate_captions, REVIEW_CAPTIONS

class CaptionTimelineTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_captions(REVIEW_CAPTIONS, 9))
    def test_gap_rejected(self):
        self.assertFalse(validate_captions([(0,2,"a"),(3,9,"b")],9))
    def test_blank_rejected(self):
        self.assertFalse(validate_captions([(0,9,"")],9))
    def test_overrun_rejected(self):
        self.assertFalse(validate_captions([(0,10,"a")],9))
if __name__ == "__main__":
    unittest.main()
