"""Review output must never be accepted as publication-ready without Japanese narration."""
import unittest
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location("render", Path(__file__).with_name("render.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ReviewTests(unittest.TestCase):
    def test_five_scenes(self):
        self.assertEqual(len(mod.SCENES), 5)
    def test_no_private_assets(self):
        self.assertTrue(all("IMG_" not in str(scene) for scene in mod.SCENES))
    def test_review_not_publication(self):
        self.assertIn("REVIEW_ONLY", Path("cycle1496_REVIEW_ONLY.mp4").name)

if __name__ == "__main__":
    unittest.main()
