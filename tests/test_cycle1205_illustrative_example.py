import tempfile
import unittest
from pathlib import Path
from tools.cycle1205_illustrative_example import build_filter, render

class DisclosureTests(unittest.TestCase):
    def test_explicit_disclosure(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"font.ttc";f.write_bytes(b"x")
            v=build_filter(str(f))
            self.assertIn("実演ではありません",v)
            self.assertIn("between(t,8,15)",v)
    def test_missing_font_rejected(self):
        with self.assertRaises(FileNotFoundError):
            build_filter("/missing/font.ttc")
    def test_missing_input_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"font.ttc";f.write_bytes(b"x")
            with self.assertRaises(FileNotFoundError):
                render(Path(d)/"missing.mp4",Path(d)/"out.mp4",str(f))
if __name__=="__main__": unittest.main()
