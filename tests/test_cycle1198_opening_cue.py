import unittest
from pathlib import Path
from src.cycle1198_opening_cue import render

class OpeningCueTests(unittest.TestCase):
    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            render(Path("/nonexistent/cycle1198.mp4"),Path("/tmp/out.mp4"))
    def test_missing_font(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/"input.mp4"
            source.write_bytes(b"placeholder")
            with self.assertRaises(FileNotFoundError):
                render(source,Path(d)/"out.mp4",font="/nonexistent/font.ttc")
