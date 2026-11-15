import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qa import check

class QualityContract(unittest.TestCase):
    def test_missing_file_fails_closed(self):
        with self.assertRaises(Exception):
            check("/nonexistent/cycle1477.mp4")

    def test_no_automatic_posting(self):
        source = Path(__file__).with_name("qa.py").read_text(encoding="utf-8")
        self.assertIn('"posting_allowed": False', source)
        self.assertIn('"japanese_narration_verified": False', source)
        self.assertIn('"speech_caption_sync_verified": False', source)

if __name__ == "__main__":
    unittest.main()
