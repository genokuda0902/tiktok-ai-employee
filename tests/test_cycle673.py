import unittest
from pathlib import Path

class Cycle673Tests(unittest.TestCase):
    def test_source_present(self):
        self.assertTrue(Path("quality/cycle673/clean_loop.py").is_file())
    def test_voice_present(self):
        self.assertTrue(Path("quality/cycle673/tts_openjtalk.py").is_file())
    def test_review_only(self):
        text=Path("quality/cycle673/clean_loop.py").read_text()
        self.assertIn("NOT_APPROVED",text)

if __name__=="__main__":
    unittest.main()
