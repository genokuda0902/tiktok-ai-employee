import unittest
from render import SCENES,SIZE
class TestRender(unittest.TestCase):
 def test_dimensions(self):self.assertEqual(SIZE,(720,1280))
 def test_scene_count(self):self.assertEqual(len(SCENES),4)
 def test_nonempty(self):self.assertTrue(all(a and b for a,b in SCENES))
if __name__=='__main__':unittest.main()
