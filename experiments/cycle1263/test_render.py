from pathlib import Path
import unittest
import ast

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "render.py"

class TestCycle1263(unittest.TestCase):
    def test_renderer_is_parseable(self):
        ast.parse(SOURCE.read_text(encoding="utf-8"))
    def test_review_only_and_no_automatic_posting(self):
        src = SOURCE.read_text(encoding="utf-8")
        self.assertIn("REVIEW ONLY", src)
        self.assertNotIn("tiktok.upload", src)
    def test_caption_and_fullhd_contract(self):
        src = SOURCE.read_text(encoding="utf-8")
        self.assertIn("1080, 1920", src)
        self.assertIn("captions.srt", src)
        self.assertIn('"-t","15"', src)

if __name__ == "__main__": unittest.main()
