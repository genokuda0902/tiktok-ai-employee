import unittest
import render
class TestReview(unittest.TestCase):
 def test_scenes(self): self.assertEqual(len(render.SCENES),5)
 def test_frame_size(self): self.assertEqual(render.draw_frame(0,0).size,(540,960))
 def test_safe_captions(self):
  for i in range(5): self.assertTrue(render.SCENES[i][1].strip())
if __name__=='__main__':unittest.main()
