import unittest
from render_cycle1264 import SCENES,W,H,FPS
class Contract(unittest.TestCase):
 def test_three_scenes(self): self.assertEqual(len(SCENES),3)
 def test_nonempty_captions(self): self.assertTrue(all(all(x.strip() for x in scene) for scene in SCENES))
 def test_vertical(self): self.assertEqual((W,H,FPS),(720,1280,15))
if __name__=="__main__":unittest.main()
