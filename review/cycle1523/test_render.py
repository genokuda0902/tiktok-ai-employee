import unittest
from pathlib import Path
from render import STEPS,DURATION,scene,draw
class ReviewTests(unittest.TestCase):
    def test_contiguous_scenes(self):
        self.assertEqual(STEPS[0][0],0)
        self.assertEqual(STEPS[-1][1],DURATION)
        self.assertTrue(all(STEPS[i][1]==STEPS[i+1][0] for i in range(len(STEPS)-1)))
    def test_transitions(self):
        self.assertEqual([scene(t) for t in (0,2,4,6,7.99)],[0,1,2,3,3])
    def test_size(self):
        self.assertEqual(draw(0).size,(720,1280))
    def test_review_gate(self):
        self.assertIn("REVIEW ONLY",Path(__file__).with_name("render.py").read_text())
if __name__=="__main__": unittest.main()
