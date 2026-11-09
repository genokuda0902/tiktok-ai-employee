import tempfile
import unittest
from pathlib import Path
from review_overlay import overlay_filter, render

class OverlayTests(unittest.TestCase):
    def test_reject_bad_duration(self):
        with self.assertRaises(ValueError):
            overlay_filter(0, __file__)
    def test_reject_missing_font(self):
        with self.assertRaises(FileNotFoundError):
            overlay_filter(15, "/missing/font.ttc")
    def test_progress_and_end_card(self):
        f = overlay_filter(15, __file__)
        self.assertIn("iw*t/15", f)
        self.assertIn("gte(t,12)", f)
    def test_no_missing_source(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                render(Path(d)/"missing.mp4", Path(d)/"out.mp4", __file__)
if __name__ == "__main__":
    unittest.main()
