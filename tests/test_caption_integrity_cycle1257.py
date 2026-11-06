import unittest
from quality.caption_integrity import validate_srt

GOOD = "1\n00:00:00,000 --> 00:00:05,000\n開始\n\n2\n00:00:05,000 --> 00:00:15,000\n終了"

class CaptionIntegrityTests(unittest.TestCase):
    def test_valid_but_not_publishable(self):
        result = validate_srt(GOOD, 15000)
        self.assertTrue(result["timing_valid"])
        self.assertFalse(result["speech_sync_verified"])
        self.assertFalse(result["posting_allowed"])

    def test_reject_overlap(self):
        with self.assertRaises(ValueError):
            validate_srt(GOOD.replace("00:00:05,000 --> 00:00:15,000", "00:00:04,000 --> 00:00:15,000"), 15000)

    def test_reject_overrun(self):
        with self.assertRaises(ValueError):
            validate_srt(GOOD, 14000)

if __name__ == "__main__":
    unittest.main()
