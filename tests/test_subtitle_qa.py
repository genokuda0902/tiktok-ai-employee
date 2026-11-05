import unittest
from tools.subtitle_qa import validate_srt

class SubtitleQATests(unittest.TestCase):
    def test_valid_japanese(self):
        s = "1\n00:00:00,000 --> 00:00:01,500\n今日はここから\n\n2\n00:00:01,500 --> 00:00:03,000\n始めましょう"
        r = validate_srt(s, 3000)
        self.assertTrue(r["passed"], r)
        self.assertFalse(r["speech_alignment_verified"])

    def test_overlap_and_overrun(self):
        s = "1\n00:00:00,000 --> 00:00:02,000\n一つ目\n\n2\n00:00:01,500 --> 00:00:04,000\n二つ目"
        r = validate_srt(s, 3000)
        self.assertFalse(r["passed"])
        self.assertTrue(any("overlaps" in e for e in r["errors"]))
        self.assertTrue(any("exceeds" in e for e in r["errors"]))

    def test_mobile_readability(self):
        s = "1\n00:00:00,000 --> 00:00:01,000\nこれはとても長すぎる日本語の字幕文章になります"
        self.assertFalse(validate_srt(s, 2000)["passed"])

    def test_bad_timestamp(self):
        s = "1\n00:99:00,000 --> 00:00:01,000\n誤り"
        self.assertFalse(validate_srt(s, 2000)["passed"])

if __name__ == "__main__":
    unittest.main()
