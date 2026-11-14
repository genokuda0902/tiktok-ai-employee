from pathlib import Path
import tempfile, unittest
from render import render

class ReviewGateTests(unittest.TestCase):
    def test_missing_approved_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                render(Path(d)/"missing.mp4",Path(d)/"output.mp4")
    def test_review_only_does_not_publish(self):
        self.assertNotIn("tiktok_upload",Path(__file__).with_name("render.py").read_text())

if __name__=="__main__": unittest.main()
