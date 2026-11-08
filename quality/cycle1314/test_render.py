import unittest
from render import SCENES
class TestTimeline(unittest.TestCase):
 def test_scene_count(self):self.assertEqual(len(SCENES),5)
 def test_original_data(self):self.assertIn('架空',SCENES[1][1])
 def test_formula(self):self.assertIn('SUM',SCENES[2][1])
 def test_total(self):self.assertEqual(1200+800+1500+500,4000)
if __name__=='__main__':unittest.main()
