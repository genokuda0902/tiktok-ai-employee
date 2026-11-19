import unittest
from render import SCENES,WIDTH,HEIGHT,FPS,DURATION
class RenderContract(unittest.TestCase):
    def test_scene_count(self): self.assertEqual(len(SCENES),4)
    def test_vertical(self): self.assertLess(WIDTH,HEIGHT)
    def test_duration(self): self.assertEqual(DURATION*FPS,192)
    def test_caption_present(self): self.assertTrue(all(a and b for a,b in SCENES))
if __name__=="__main__": unittest.main()
