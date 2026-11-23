import unittest
from pathlib import Path
from render import SCENES
class QualityContract(unittest.TestCase):
 def test_three_scenes(self):self.assertEqual(len(SCENES),3)
 def test_japanese(self):self.assertTrue(all(any(ord(c)>0x3000 for c in s[1]) for s in SCENES))
 def test_review_only(self):self.assertIn("REVIEW ONLY",Path(__file__).with_name("render.py").read_text())
 def test_no_approval(self):self.assertNotIn("PUBLICATION_APPROVED",Path(__file__).with_name("render.py").read_text())
if __name__=="__main__":unittest.main()
