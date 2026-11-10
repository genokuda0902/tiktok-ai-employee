import unittest
from render import SCENES
class TestSceneTiming(unittest.TestCase):
 def test_duration(self):self.assertEqual(sum(x[2] for x in SCENES),12)
 def test_no_empty_caption(self):self.assertTrue(all(x[0] and x[1] for x in SCENES))
 def test_four_scenes(self):self.assertEqual(len(SCENES),4)
if __name__=='__main__':unittest.main()
