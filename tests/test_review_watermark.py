import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.review_watermark import render

class WatermarkTests(unittest.TestCase):
    def test_missing_source_rejected(self):
        with TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                render(Path(d)/"missing.mp4", Path(d)/"out.mp4")
    def test_no_output_on_failure(self):
        with TemporaryDirectory() as d:
            out=Path(d)/"out.mp4"
            with self.assertRaises(FileNotFoundError):
                render(Path(d)/"missing.mp4",out)
            self.assertFalse(out.exists())
