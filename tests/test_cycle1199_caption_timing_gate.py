import unittest
from tools.cycle1199_caption_timing_gate import check_srt, seconds

def cue(a="00:00:00,000", b="00:00:01,000", text="こんにちは"):
    return f"1\n{a} --> {b}\n{text}\n"

class CaptionTimelineTests(unittest.TestCase):
    def test_valid_japanese_cue(self):
        self.assertTrue(check_srt(cue(), 2.0)["passed"])
    def test_rejects_out_of_bounds(self):
        self.assertFalse(check_srt(cue(b="00:00:03,000"), 2.0)["passed"])
    def test_rejects_too_short(self):
        self.assertFalse(check_srt(cue(b="00:00:00,100"), 2.0)["passed"])
    def test_rejects_overlap(self):
        s = cue() + "\n2\n00:00:00,900 --> 00:00:02,000\n次の字幕\n"
        self.assertFalse(check_srt(s, 3.0)["passed"])
    def test_rejects_invalid_timestamp(self):
        with self.assertRaises(ValueError):
            seconds("00:70:00,000")

if __name__ == "__main__":
    unittest.main()
