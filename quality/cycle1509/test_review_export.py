import unittest
from pathlib import Path
from review_export import FILTER, render
class TestReviewExport(unittest.TestCase):
    def test_dimensions(self): self.assertIn("scale=1080:1920", FILTER)
    def test_frame_rate(self): self.assertIn("fps=24", FILTER)
    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError): render(Path("/missing/input.mp4"),Path("/tmp/no.mp4"))
if __name__=="__main__": unittest.main()
