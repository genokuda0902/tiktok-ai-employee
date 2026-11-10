import unittest
from render import STEPS, make_frame
class RenderTests(unittest.TestCase):
    def test_four_scenes(self): self.assertEqual(len(STEPS),4)
    def test_vertical_resolution(self): self.assertEqual(make_frame(0).size,(720,1280))
    def test_nonempty_captions(self): self.assertTrue(all(a and b for a,b in STEPS))
if __name__=="__main__": unittest.main()
