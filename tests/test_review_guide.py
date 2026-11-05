import tempfile
import unittest
from pathlib import Path
from src.review_guide import review_filter, render

class ReviewGuideTests(unittest.TestCase):
    def test_missing_font_rejected(self):
        with self.assertRaises(ValueError):
            review_filter("/does/not/exist.ttf")
    def test_timing_and_safe_zone(self):
        with tempfile.NamedTemporaryFile(suffix=".ttf") as f:
            result = review_filter(f.name)
            self.assertIn("between(t,4,8)", result)
            self.assertIn("between(t,13,17)", result)
            self.assertIn("y=400", result)
    def test_missing_source_rejected(self):
        with tempfile.NamedTemporaryFile(suffix=".ttf") as f:
            with self.assertRaises(FileNotFoundError):
                render(Path("/not/found.mp4"), Path("/tmp/unused.mp4"), f.name)
if __name__ == "__main__":
    unittest.main()
