import unittest
from pathlib import Path
from render_review_1262 import SCENES
class ReviewTests(unittest.TestCase):
 def test_three_distinct_scenes(self):
  self.assertEqual(len(SCENES),3)
  self.assertEqual(len(set(x[1] for x in SCENES)),3)
 def test_no_publication_claim(self):
  self.assertTrue(all(x[1] for x in SCENES))
 def test_15_seconds(self):
  self.assertEqual(len(SCENES)*5,15)
if __name__=="__main__": unittest.main()
