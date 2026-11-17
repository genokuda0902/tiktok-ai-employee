import unittest
from render import SCENES,scene,frame
class TestRender(unittest.TestCase):
 def test_scenes(self):
  self.assertEqual(len(SCENES),3)
  for a,b,_,_ in SCENES:self.assertLess(a,b)
 def test_timing(self):
  self.assertEqual(scene(0)[2],SCENES[0][2]);self.assertEqual(scene(7.9)[2],SCENES[2][2])
 def test_frame(self):self.assertEqual(frame(3).size,(720,1280))
if __name__=="__main__":unittest.main()
