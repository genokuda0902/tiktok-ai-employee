import unittest
import render
class TestReview(unittest.TestCase):
 def test_scenes(self): self.assertEqual(len(render.SCENES),5)
 def test_frame_size(self): self.assertEqual(render.draw_frame(0,0).size,(540,960))
 def test_caption_presence(self):
  for title,caption in render.SCENES:
   self.assertTrue(title.strip());self.assertTrue(caption.strip())
 def test_hook_changed(self): self.assertIn('手計算',render.SCENES[0][0])
if __name__=='__main__': unittest.main()
