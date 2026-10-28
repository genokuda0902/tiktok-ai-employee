import unittest
from template_story import *
class RendererTests(unittest.TestCase):
 def test_ten_genres(self): self.assertTrue(validate())
 def test_frames(self):
  for i in (0,12,25,26,40,51,52,65,77):
   im=frame(i);self.assertEqual(im.size,(1080,1260))
 def test_stages_change(self):
  a,b,c=(frame(i) for i in (10,36,63))
  self.assertNotEqual(a.tobytes(),b.tobytes());self.assertNotEqual(b.tobytes(),c.tobytes())
 def test_genre_changes(self): self.assertNotEqual(frame(36,'ai_work').tobytes(),frame(36,'travel').tobytes())
 def test_bounds(self):
  with self.assertRaises(ValueError):frame(-1)
  with self.assertRaises(ValueError):frame(78)
  with self.assertRaises(ValueError):frame(0,'unknown')
 def test_caption_safe(self):self.assertLess(Y0+H,SAFE_CAPTION_Y)
if __name__=='__main__':unittest.main()
