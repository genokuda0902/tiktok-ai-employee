import tempfile
import unittest
from pathlib import Path
from subtitle_gate import validate_srt

class SubtitleGateTests(unittest.TestCase):
    def test_valid(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"x.srt"
            p.write_text("1\n00:00:00,000 --> 00:00:03,000\n日本語字幕\n", encoding="utf-8")
            self.assertTrue(validate_srt(str(p), 1))
    def test_missing_japanese_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"x.srt"
            p.write_text("1\n00:00:00,000 --> 00:00:03,000\nEnglish only\n", encoding="utf-8")
            self.assertFalse(validate_srt(str(p), 1))
if __name__ == "__main__": unittest.main()
