import unittest
from render import SCENES
class TestStoryboard(unittest.TestCase):
 def test_scene_count(self): self.assertEqual(len(SCENES),5)
 def test_no_empty_captions(self): self.assertTrue(all(a and b for a,b,_ in SCENES))
 def test_disclosure(self): self.assertIn("架空",SCENES[-1][1])
if __name__=="__main__":unittest.main()
