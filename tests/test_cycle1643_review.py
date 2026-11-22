"""Tests for cycle1643 review generator; no network, no private assets."""
import unittest
from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("review",ROOT/"tools/cycle1643_review.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ReviewTests(unittest.TestCase):
    def test_five_scenes(self):
        self.assertEqual(len(mod.SCENES),5)
    def test_explicit_before_after(self):
        self.assertEqual([x[0] for x in mod.SCENES][1:3],["BEFORE","AFTER"])
    def test_no_real_personal_data(self):
        text=" ".join(" ".join(s) for s in mod.SCENES)
        self.assertNotIn("@",text)
        self.assertNotIn("https://",text)
    def test_review_gate(self):
        import inspect
        src=inspect.getsource(mod.verify)
        self.assertIn('"posting_allowed":False',src)
        self.assertIn('"japanese_narration":False',src)

if __name__=="__main__":
    unittest.main()
