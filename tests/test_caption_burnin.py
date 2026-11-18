import unittest
from src.caption_burnin import validate_srt

class CaptionTest(unittest.TestCase):
    def test_valid(self):
        validate_srt("1\n00:00:00,000 --> 00:00:01,000\nこんにちは")
    def test_no_timing(self):
        with self.assertRaises(ValueError): validate_srt("こんにちは")
    def test_no_japanese(self):
        with self.assertRaises(ValueError): validate_srt("1\n00:00:00,000 --> 00:00:01,000\nhello")
if __name__ == "__main__": unittest.main()
