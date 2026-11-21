import unittest
from render import frame,SCENES,FPS,W,H
class TestRender(unittest.TestCase):
 def test_scene_count(self):self.assertEqual(len(SCENES),5)
 def test_dimensions(self):self.assertEqual(frame(0).size,(W,H))
 def test_timing(self):self.assertEqual(FPS,24);self.assertEqual(len(SCENES)*3,15)
 def test_synthetic(self):self.assertIn("架空",SCENES[1][1])
if __name__=="__main__":unittest.main()
