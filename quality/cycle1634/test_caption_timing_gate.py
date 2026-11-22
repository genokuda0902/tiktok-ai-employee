import tempfile
import unittest
from pathlib import Path
from caption_timing_gate import validate_srt

class TimingGateTests(unittest.TestCase):
    def check(self, text):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"captions.srt"
            path.write_text(text,encoding="utf-8")
            return validate_srt(path,expected_seconds=6)
    def test_contiguous(self):
        self.assertEqual(self.check("1\n00:00:00,000 --> 00:00:03,000\nA\n\n2\n00:00:03,000 --> 00:00:06,000\nB\n"),2)
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):
            self.check("1\n00:00:00,000 --> 00:00:02,000\nA\n\n2\n00:00:03,000 --> 00:00:06,000\nB\n")
    def test_missing_final_seconds_rejected(self):
        with self.assertRaises(ValueError):
            self.check("1\n00:00:00,000 --> 00:00:03,000\nA\n")
if __name__=="__main__":unittest.main()
