import unittest
from render import SCENES,scene_at,draw_frame,WIDTH,HEIGHT
class Tests(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual([scene_at(x) for x in [0,2.99,3,5.99,6,8.99]],[0,0,1,1,2,2])
    def test_frame_dimensions(self):
        self.assertEqual(draw_frame(0).size,(WIDTH,HEIGHT))
    def test_disclosure(self):
        self.assertIn("未実装",SCENES[-1][1]+SCENES[-1][2])
if __name__=="__main__": unittest.main()
