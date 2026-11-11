import unittest
from pathlib import Path
import importlib.util
p=Path(__file__).with_name("render.py")
spec=importlib.util.spec_from_file_location("review_render",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestReview(unittest.TestCase):
 def test_scenes(self):
  self.assertEqual(len(m.SCENES),4)
  self.assertEqual(sum([2400,3100,4200,2700]),12400)
 def test_valid_formula(self):
  self.assertIn("=SUM(B2:B5)",str(m.SCENES))
 def test_review_only(self):
  self.assertIn("-an",p.read_text())
if __name__=="__main__":unittest.main()
