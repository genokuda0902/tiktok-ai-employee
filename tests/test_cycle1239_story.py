import unittest
from src.cycle1239_story import scene_plan, validate, SCENES
class StoryTest(unittest.TestCase):
 def test_sequence(self):
  self.assertEqual([x["label"] for x in scene_plan()],["BEFORE","ACTION","AFTER"])
 def test_timing(self):
  self.assertEqual(scene_plan()[-1]["end"],18)
 def test_bad_order(self):
  with self.assertRaises(ValueError): validate(list(reversed(SCENES)))
if __name__=="__main__": unittest.main()
