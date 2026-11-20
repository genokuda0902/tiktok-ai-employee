import unittest
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location("render",Path(__file__).with_name("render.py"))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ReviewTests(unittest.TestCase):
 def test_three_scenes(self): self.assertEqual(len(m.SCENES),3)
 def test_no_private_media(self): self.assertNotIn("IMG_5805",Path(m.__file__).read_text())
 def test_review_only(self): self.assertIn("REVIEW ONLY",Path(m.__file__).read_text())
 def test_japanese_copy(self): self.assertTrue(all(any(ord(c)>127 for c in s[0]) for s in m.SCENES))
if __name__=="__main__": unittest.main()
